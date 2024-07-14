import os
import json

from plugins import Database, Wakachigaki, VoicevoxConnecter
from logging import getLogger, config

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

#ログの準備
with open(os.path.join(currentDir, "setting", "log_config.json"), 'r') as f:
    log_conf = json.load(f)

config.dictConfig(log_conf)
logger = getLogger(__name__)

def generate(text, filename):
    
    if(os.path.isdir(os.path.join(currentDir, "app", "audio", "separates")) == False):
        os.mkdir(os.path.join(currentDir, "app", "audio", "separates"))
    
    phonemes = Wakachigaki.moraWakachi(text)
    logger.info("音素数 : {}".format(str(phonemes)))
    
    if not (text == ""):
        response = VoicevoxConnecter.render_voice(text)

    if not response == None:
        Database.temp_data_push(filename, os.path.join(currentDir, "app", "audio", "separates", filename), text, phonemes)
        
        with open(os.path.join(currentDir, "app", "audio", "separates", filename), "wb") as fp:
            fp.write(response)

        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "audio", "separates", filename)