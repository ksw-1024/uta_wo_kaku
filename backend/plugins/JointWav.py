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
    
    if(l == 0):
        return
    
    i = 0
    done_time = 0
    while (i < (l - 1)):
        logger.info("{}番目の処理を開始".format(str(i+1)))
        onnso = DB.get_info_row("temp_audio", "filename", os.path.basename(inputs[i][0]))[0][5]
        
        sound1 = AudioSegment.from_file(inputs[i][0])
        sound2 = AudioSegment.from_file(inputs[i+1][0])
        
        if (onnso <= 4):
            silent_temp = AudioSegment.silent(duration=400)
            sound1 = sound1 + silent_temp
        
            output_dir = inputs[i+1][0]
        
            output_temp = sound1.overlay(sound2, position=(400 + done_time))
            output_temp.export(output_dir, format="wav")
            
            done_time = done_time + 400
        else:
            silent_temp = AudioSegment.silent(duration=800)
            sound1 = sound1 + silent_temp
        
            output_dir = inputs[i+1][0]
        
            output_temp = sound1.overlay(sound2, position=(800 + done_time))
            output_temp.export(output_dir, format="wav")
            
            done_time = done_time + 800
        
        i = i + 1
    
    Audio = AudioSegment.from_wav(inputs[l-1][0])
    silent = AudioSegment.silent(duration=1580)
    c = silent + Audio
    c.export(output, format="wav")
    
    for i in inputs:
        fn = os.path.basename(i[0])
        word = DB.get_info_row("temp_audio", "filename", fn)[0][4]
        DB.data_push(os.path.basename(output), fn, word)
        DB.history_data_push(os.path.basename(output), word)
        
    #temp_audioを削除
    shutil.rmtree(os.path.join(currentDir, "app", "audio", "separates"))
    os.mkdir(os.path.join(currentDir, "app", "audio", "separates"))
    
    DB.delete_table("temp_audio")