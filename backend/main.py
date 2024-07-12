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

from logging import getLogger, config

#自分の関数読み出し

from plugins import VoiceGenerater, Wakachigaki, JointWav, Database

currentDir = os.path.dirname(os.path.abspath(__file__))

platform_info = "NoData"

pf = platform.system()
if pf == "Windows":
    platform_info = "Windows"
elif pf == "Darwin":
    platform_info = "macOS"
elif pf == "Linux":
    platform_info = "Linux"

with open(os.path.join(currentDir, "onomatope_list.csv"), encoding="utf-8") as f:
    reader = csv.reader(f)
    onomatope_list = [row for row in reader]
    
with open(os.path.join(currentDir, "setting", "log_config.json"), 'r') as f:
    log_conf = json.load(f)

config.dictConfig(log_conf)
logger = getLogger(__name__)
    
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
    latest_file = Database.get_info("audio", "id", "1")[0][2]
    
    return send_from_directory("audio", latest_file)

@app.route("/render_voice", methods=["POST"])  #追加
def render():
    voicetext = request.get_json()
    text = voicetext["text"]
    
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    filename = dt_now + ".wav"
    return_data = {"fileUrl": VoiceGenerater.generate(text, filename=filename)}
    return jsonify(return_data)

@app.route("/glue", methods=["POST"])
def glue():
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
    logger.info("== Activate onomatopoeia auto-generation mode ==")
    mode_data = request.get_json()
    count = mode_data["count"]
    
    for i in range(count):
        word = onomatope_list[random.randint(0, 276)][0]
        logger.info("{0} generated word : {1}".format(str(i+1), word))
        logger.info("Start to generate file")
        
        dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = dt_now + ".wav"
        logger.info("セパレートファイル名 : {}".format(filename))
        
        VoiceGenerater.generate(word, filename)
        logger.info("セパレートファイル生成完了")
        logger.info("次の作業に移行します")
        
    logger.info("ファイルの結合を開始します")
    
    files = glob.glob(os.path.join(currentDir, "audio", "separates", "*"))

    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = dt_now + ".wav"
    
    JointWav.joint_audio(files, os.path.join(currentDir,"audio", filename))
    logger.info("結合完了 : 完成したファイル名 -> {}".format(filename))
    logger.info("以上で動作を終了します")
    
    return_data = {"fileUrl": os.path.join(currentDir, "audio", filename)}
    return jsonify(return_data)

if __name__ == '__main__':
    app.run(port=8888)