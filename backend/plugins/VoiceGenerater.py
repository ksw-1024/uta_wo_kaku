import os

import requests
import json

from logging import getLogger, config

from plugins import Database, Wakachigaki

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

with open(os.path.join(currentDir, "setting", "log_config.json"), 'r') as f:
    log_conf = json.load(f)

config.dictConfig(log_conf)
logger = getLogger(__name__)

def generate(text, filename, speaker=1):
    
    if(os.path.isdir(os.path.join(currentDir, "audio", "separates")) == False):
        os.mkdir(os.path.join(currentDir, "audio", "separates"))
    
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
    query["pitchScale"] = 0.06
    
    phonemes = Wakachigaki.moraWakachi(text)
    logger.info("音素数 : {}".format(str(phonemes)))
    
    # 合成された音声データを取得
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(query)
    )

    if response2.status_code == 200:
        Database.temp_data_push(filename, os.path.join(currentDir, "audio", "separates", filename), text, phonemes)
        
        with open(os.path.join(currentDir, "audio", "separates", filename), "wb") as fp:
            fp.write(response2.content)

        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "separates", filename)