import os
import platform

import json
import datetime
import shutil

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

from pydub import AudioSegment

import glob
import wave

import random
import sys

currentDir = os.path.dirname(os.path.abspath(__file__))

jp = ["あ","い","う","え","お","か","き","く","け","こ","さ","し","す","せ","そ","た","ち","つ","て","と","な","に","ぬ","ね","の","は","ひ","ふ","へ","ほ","ま","み","む","め","も","や","ゆ","よ","ら","り","る","れ","ろ","わ","を","ん"]

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
    if (time > 0 and time <= 400):
        sourceAudio = sourceAudio[93:time]
        silent = AudioSegment.silent(duration=((400 - time) + 93))
        c = sourceAudio + silent
    elif (time <= 800):
        sourceAudio = sourceAudio[93:time]
        silent = AudioSegment.silent(duration=((800 - time) + 93))
        c = sourceAudio + silent
    else:
        c = sourceAudio[93:893]
    c.export(output_path, format="wav")
    
def join_audio(inputs, output):
    fps = [wave.open(f, 'r') for f in inputs]
    fpw = wave.open(output, 'w')

    fpw.setnchannels(fps[0].getnchannels())
    fpw.setsampwidth(fps[0].getsampwidth())
    fpw.setframerate(fps[0].getframerate())
        
    for fp in fps:
        fpw.writeframes(fp.readframes(fp.getnframes()))
        fp.close()
    fpw.close()
    
    Audio = AudioSegment.from_wav(output)
    silent = AudioSegment.silent(duration=1600)
    c = silent + Audio
    c.export(output, format="wav")
    
def make_word(length,words):
    word = ""
    for i in range(length):
        word += words[random.randint(0,len(words)-1)]
    return word
    
app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False

@app.route("/render_voice", methods=["POST"])  #追加
def render():
    json = request.get_json()
    text = json["text"]
    
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
    json = request.get_json()
    count = json["count"]
    length = json["length"]
    
    for i in range(count):
        word = make_word(length, jp)
        print(str(i+1) + "番目に生成したワード : " + word)
        print("ファイルの生成開始")
        
        dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = dt_now + ".wav"
        print("セパレートファイル名 : " + filename)
        
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
    
    return_data = {"fileUrl": os.path.join(currentDir, "audio", filename)}
    return jsonify(return_data)

if __name__ == '__main__':
    app.run()