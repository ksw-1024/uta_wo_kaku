import os
import platform

import json
import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

from pydub import AudioSegment

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

    headers = {'Content-Type': 'application/json',}

    # 合成された音声データを取得
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    # WAVファイル再生部分
    if response2.status_code == 200:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("temp/audio")
        with open(filename, "wb") as fp:
            fp.write(response2.content)
        add_silence_to_audio(os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio/separates"), os.path.join(os.path.dirname))
        return os.path.join(os.getcwd(), filename)
    
def add_silence_to_audio(output_path, input_path, msec):
    sourceAudio = AudioSegment.from_wav(input_path)
    time = (msec - len(sourceAudio))
    if(time>0):
        silent = AudioSegment.silent(duration=time)
        c = sourceAudio + silent
    else:
        c = sourceAudio[:5000]
    c.export(output_path, format="wav")

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

if __name__ == '__main__':
    app.run()