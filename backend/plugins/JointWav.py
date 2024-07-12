import os
import shutil

from pydub import AudioSegment

from logging import getLogger, config
import json

from plugins import Database as DB

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

with open(os.path.join(currentDir, "setting", "log_config.json"), 'r') as f:
    log_conf = json.load(f)

config.dictConfig(log_conf)
logger = getLogger(__name__)

def joint_audio(inputs, output):
    l = len(inputs)
    i = 0
    while (i < (l - 1)):
        logger.info("{}番目の処理を開始".format(str(i+1)))
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
    
    #データベースへの登録
    DB.delete_table("audio")
    
    for i in inputs:
        fn = os.path.basename(i)
        word = DB.get_info("temp_audio", "filename", fn)[0][3]
        DB.data_push(os.path.basename(output), fn, word)
    
    #Sepatateファイルの中身を削除
    if(os.path.isdir(os.path.join(currentDir, "audio", "separates"))):
        DB.delete_table("temp_audio")
        
        logger.info("ファイルの削除を実行します")
        shutil.rmtree(os.path.join(currentDir, "audio", "separates"))
        os.mkdir(os.path.join(currentDir, "audio", "separates"))