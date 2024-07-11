import os
import platform

import json
import datetime
import shutil

from flask import Flask, jsonify, request, render_template, send_from_directory, url_for
from flask_cors import CORS
import requests

from pydub import AudioSegment

import glob
import wave

import csv
import random

import re

currentDir = os.path.dirname(os.path.abspath(__file__))

c1 = '[ウクスツヌフムユルグズヅブプヴ][ァィェォ]' #ウ段＋「ァ/ィ/ェ/ォ」
c2 = '[イキシチニヒミリギジヂビピ][ャュェョ]' #イ段（「イ」を除く）＋「ャ/ュ/ェ/ョ」
c3 = '[テデ][ィュ]' #「テ/デ」＋「ャ/ィ/ュ/ョ」
c4 = '[ァ-ヴー]' #カタカナ１文字（長音含む）

cond = '('+c1+'|'+c2+'|'+c3+'|'+c4+')'
re_mora = re.compile(cond)

def moraWakachi(kana_text):
    return re_mora.findall(kana_text)

with open(os.path.join(currentDir, "onomatope_list.csv")) as f:
    reader = csv.reader(f)
    onomatope_list = [row for row in reader]

def generate_and_play_wav(text, filename, speaker=1):
    host = 'localhost'
    port = 50021
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    
    # 音声合成のためのクエリを送信
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )

    headers = {'Content-Type': 'application/json'}
    
    query = response1.json()
    query["speedScale"] = 1.6
    query["prePhonemeLength"] = 0
    query["pitchScale"] = 0.02
    
    phonemes = len(query["accent_phrases"][0]["moras"])
    print("音素数 : " + str(phonemes))
    
    # 合成された音声データを取得
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(query)
    )

    # WAVファイル再生部分
    if response2.status_code == 200:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("temp/audio")
        with open(filename, "wb") as fp:
            fp.write(response2.content)
        add_silence_to_audio(os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "separates", filename), os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp", "audio", filename))
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "separates", filename)
    
def add_silence_to_audio(output_path, input_path):
    sourceAudio = AudioSegment.from_wav(input_path)
    time = len(sourceAudio)
    if(os.path.isdir(os.path.join(currentDir, "audio", "separates")) == False):
        os.mkdir(os.path.join(currentDir, "audio", "separates"))
        
    # if (time > 0 and time <= 400):
    #     sourceAudio = sourceAudio[93:time]
    #     silent = AudioSegment.silent(duration=((400 - time) + 93))
    #     c = sourceAudio + silent
    # elif (time <= 800):
    #     sourceAudio = sourceAudio[93:time]
    #     silent = AudioSegment.silent(duration=((800 - time) + 93))
    #     c = sourceAudio + silent
    # else:
    #     c = sourceAudio[93:893]
    
    sourceAudio.export(output_path, format="wav")
    
def join_audio(inputs, output):
    print(inputs)
    l = len(inputs)
    print(l)
    i = 0
    while (i < (l - 1)):
        print(str(i+1) + "番目の処理を開始")
        sound1 = AudioSegment.from_file(inputs[i])
        sound2 = AudioSegment.from_file(inputs[i+1])
        
        silent_temp = AudioSegment.silent(duration=400)
        sound1 = sound1 + silent_temp
        
        output_dir = inputs[i+1]
        
        output_temp = sound1.overlay(sound2, position=(390 + i*400))
        output_temp.export(output_dir, format="wav")
        
        i = i + 1
    
    Audio = AudioSegment.from_wav(inputs[l-1])
    silent = AudioSegment.silent(duration=1590)
    c = silent + Audio
    c.export(output, format="wav")
    
app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False

@app.route("/")
def display():
    html = render_template("index.html")
    return html

@app.route("/audio/bgm.mp3")
def play_bgm():
    return send_from_directory("audio", "bgm.mp3")

@app.route("/audio/voice.wav")
def  voice_data():
    with open(os.path.join(currentDir, "temp", "json", "filename.json")) as f:
        d = json.load(f)
    
    latest_file = d["filename"]
    return send_from_directory("audio", latest_file)

@app.route("/render_voice", methods=["POST"])  #追加
def render():
    voicetext = request.get_json()
    text = voicetext["text"]
    
    pf = platform.system()
    if pf == "Windows":
        print("on Windows")
    else:
        print("not Windows")
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    filename = dt_now + ".wav"
    return_data = {"fileUrl": generate_and_play_wav(text, filename=filename)}
    return jsonify(return_data)

@app.route("/glue", methods=["POST"])
def glue():
    pf = platform.system()
    if pf == "Windows":
        print("on Windows")
    else:
        print("not Windows")
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    files = glob.glob(os.path.join(currentDir, "audio", "separates", "*"))
    for file in files:
        print(file)
    
    filename = dt_now + ".wav"
    
    join_audio(files, os.path.join(currentDir,"audio", filename))
    
    #Tempファイルの中身を削除
    if(os.path.isdir(os.path.join(currentDir, "temp", "audio"))):
        shutil.rmtree(os.path.join(currentDir, "temp", "audio"))
        os.mkdir(os.path.join(currentDir, "temp", "audio"))
    
    return_data = {"fileUrl": os.path.join(currentDir, "audio", filename)}
    return jsonify(return_data)

@app.route("/auto_onomatope", methods=["POST"])
def auto_onomatope():
    print("== オノマトペ自動生成モードを起動します ==")
    mode_data = request.get_json()
    count = mode_data["count"]
    
    toJson = {"filename": "", "word": {}}
    
    for i in range(count):
        word = onomatope_list[random.randint(0, 276)][0]
        print(str(i+1) + "番目に生成したワード : " + word)
        print("ファイルの生成開始")
        
        dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = dt_now + ".wav"
        print("セパレートファイル名 : " + filename)
        
        toJson["word"][i] = word
        
        generate_and_play_wav(word, filename)
        print("セパレートファイル生成完了")
        print("次の作業に移行します")
        
    print("ファイルの結合を開始します")
    
    files = glob.glob(os.path.join(currentDir, "audio", "separates", "*"))
    for file in files:
        print(file)
    print("ファイルリスト取得完了")
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = dt_now + ".wav"
    
    join_audio(files, os.path.join(currentDir,"audio", filename))
    print("結合完了 : 完成したファイル名 -> " + filename)
    print("以上で動作を終了します")
    
    #Tempファイルの中身を削除
    if(os.path.isdir(os.path.join(currentDir, "temp", "audio"))):
        shutil.rmtree(os.path.join(currentDir, "temp", "audio"))
        os.mkdir(os.path.join(currentDir, "temp", "audio"))
        
    #Sepatateファイルの中身を削除
    if(os.path.isdir(os.path.join(currentDir, "audio", "separates"))):
        shutil.rmtree(os.path.join(currentDir, "audio", "separates"))
        os.mkdir(os.path.join(currentDir, "audio", "separates"))
    
    toJson["filename"] = filename
    with open(os.path.join(currentDir, "temp", "json", "filename.json"), "w") as f:
        json.dump(toJson, f, indent=2, ensure_ascii=False)
    
    return_data = {"fileUrl": os.path.join(currentDir, "audio", filename)}
    return jsonify(return_data)

if __name__ == '__main__':
    app.run(port=8888)