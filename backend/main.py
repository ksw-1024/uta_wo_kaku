import os
import platform

import json
import datetime
import shutil

from flask import Flask, jsonify, request, render_template, send_from_directory, url_for
from flask_cors import CORS

import glob

import csv
import random

#自分の関数読み出し

from plugins import VoiceGenerater, Wakachigaki, JointWav

currentDir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(currentDir, "onomatope_list.csv"), encoding="utf-8") as f:
    reader = csv.reader(f)
    onomatope_list = [row for row in reader]
    
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
    return_data = {"fileUrl": VoiceGenerater.generate(text, filename=filename)}
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
    
    JointWav.joint_audio(files, os.path.join(currentDir,"audio", filename))
    
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
        
        VoiceGenerater.generate(word, filename)
        print("セパレートファイル生成完了")
        print("次の作業に移行します")
        
    print("ファイルの結合を開始します")
    
    files = glob.glob(os.path.join(currentDir, "audio", "separates", "*"))
    for file in files:
        print(file)
    print("ファイルリスト取得完了")
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = dt_now + ".wav"
    
    JointWav.joint_audio(files, os.path.join(currentDir,"audio", filename))
    print("結合完了 : 完成したファイル名 -> " + filename)
    print("以上で動作を終了します")
    
    toJson["filename"] = filename
    with open(os.path.join(currentDir, "temp", "json", "filename.json"), "w", encoding="utf-8") as f:
        json.dump(toJson, f, indent=2, ensure_ascii=False)
    
    return_data = {"fileUrl": os.path.join(currentDir, "audio", filename)}
    return jsonify(return_data)

if __name__ == '__main__':
    app.run(port=8888)