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

currentDir = os.path.dirname(os.path.abspath(__file__))

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
        add_silence_to_audio(os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "separates", filename), os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp", "audio", filename), 400)
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "separates", filename)
    
def add_silence_to_audio(output_path, input_path, msec):
    sourceAudio = AudioSegment.from_wav(input_path)
    time = (msec - len(sourceAudio))
    if(time > 0):
        sourceAudio = sourceAudio[93:len(sourceAudio)]
        silent = AudioSegment.silent(duration=(time + 93))
        c = sourceAudio + silent
    else:
        c = sourceAudio[93:493]
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

if __name__ == '__main__':
    app.run()