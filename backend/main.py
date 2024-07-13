import os
import platform

import json
import datetime

from flask import Flask, jsonify, request, render_template, send_from_directory, url_for
from flask_cors import CORS

import csv
import random

from logging import getLogger, config

import threading

#自分の関数読み出し

from plugins import VoiceGenerater, Wakachigaki, JointWav, Database, KinshiWord

currentDir = os.path.dirname(os.path.abspath(__file__))

#プラットフォームの情報取得
platform_info = "NoData"

pf = platform.system()
if pf == "Windows":
    platform_info = "Windows"
elif pf == "Darwin":
    platform_info = "macOS"
elif pf == "Linux":
    platform_info = "Linux"

#オノマトペリストを取得
with open(os.path.join(currentDir, "onomatope_list.csv"), encoding="utf-8") as f:
    reader = csv.reader(f)
    onomatope_list = [row for row in reader]
    
#ログの準備
with open(os.path.join(currentDir, "setting", "log_config.json"), 'r') as f:
    log_conf = json.load(f)

config.dictConfig(log_conf)
logger = getLogger(__name__)
    
app = Flask(__name__, static_folder=os.path.join(currentDir, "static"))
CORS(app)
app.config["JSON_AS_ASCII"] = False
     
def joint_threads():
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    files = Database.get_info_column("filepath", "temp_audio")
    filename = dt_now + ".wav"
    
    JointWav.joint_audio(files, os.path.join(currentDir,"audio", filename))
                
@app.route("/")
def home_page():
    try:
        t_format = "%Y-%m-%d %H:%M:%S%z"
        dt_latest = datetime.datetime.strptime(Database.get_info_latest("audio")[0][2]+"+0000", t_format)
    except:
        logger.warning("時間の変換・取得に失敗")
        try:
            t_format = "%Y-%m-%d %H:%M:%S%z"
            dt_latest = datetime.datetime.strptime(Database.get_info_latest("temp_audio")[0][2]+"+0000", t_format)
        except:
            logger.error("処理されていないセパレートファイルが見つかりませんでした")
        else:
            logger.info("セパレートファイルを確認、処理を継続します")       
    
    dt_now = datetime.datetime.now(datetime.timezone.utc)
    try:
        td = dt_now - dt_latest
    except:
        logger.error("時間の計算に失敗")
    else:
        print(td)
        print(td.total_seconds())
        if(td.total_seconds() > 300):
            thread = threading.Thread(target=joint_threads)
            thread.start()
            logger.info("結合処理を開始します")
        else:
            logger.info("前回の結合から時間が空いていません")
        
    html = render_template("index.html")
    return html

@app.route("/create")
def create_page():
    html = render_template("create/index.html")
    return html

@app.route("/play")
def play_page():
    html = render_template("play/index.html")
    return html

@app.route("/about")
def about_page():
    html = render_template("about/index.html")
    return html

@app.route("/audio/bgm.mp3")
def play_bgm():
    return send_from_directory("audio", "bgm.mp3")

@app.route("/audio/voice.wav")
def  voice_data():
    latest_file = Database.get_info_row("audio", "id", "1")[0][2]
    
    return send_from_directory("audio", latest_file)

@app.route("/history", methods=["POST"])
def history():
    fn = Database.get_info_row("audio", "id", "1")[0][2]
    wordlist = Database.get_info_row("history", "filename", fn)
    
    return jsonify(wordlist)

@app.route("/render_voice", methods=["POST"])  #追加
def render():
    voicetext = request.get_json()
    text = voicetext["text"]
    
    if(KinshiWord.is_ng(text)):
        return_data = {"fileUrl": "THIS IS NG WORD"}
        return jsonify(return_data)
    
    if(Wakachigaki.moraWakachi(text) > 8):
        return_data = {"fileUrl": "TOO MANY LETTERS"}
        return jsonify(return_data)
    
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    filename = dt_now + ".wav"
    return_data = {"fileUrl": VoiceGenerater.generate(text, filename=filename)}
    return jsonify(return_data)

@app.route("/glue", methods=["POST"])
def glue():
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    files = Database.get_info_column("filepath", "temp_audio")
    filename = dt_now + ".wav"
    
    JointWav.joint_audio(files, os.path.join(currentDir,"audio", filename))
    
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
    
    files = Database.get_info_column("filepath", "temp_audio")

    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = dt_now + ".wav"
    
    JointWav.joint_audio(files, os.path.join(currentDir,"audio", filename))
    logger.info("結合完了 : 完成したファイル名 -> {}".format(filename))
    logger.info("以上で動作を終了します")
    
    return_data = {"fileUrl": os.path.join(currentDir, "audio", filename)}
    return jsonify(return_data)

if __name__ == '__main__':
    app.run(port=8888)