import os

from plugins import Database, Wakachigaki, VoicevoxConnecter
from main import logger

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

def generate(text, filename):
    
    if(os.path.isdir(os.path.join(currentDir, "audio", "separates")) == False):
        os.mkdir(os.path.join(currentDir, "audio", "separates"))
    
    phonemes = Wakachigaki.moraWakachi(text)
    logger.info("音素数 : {}".format(str(phonemes)))
    
    if not (text == ""):
        response = VoicevoxConnecter.render_voice(text)

    if not response == None:
        Database.temp_data_push(filename, os.path.join(currentDir, "audio", "separates", filename), text, phonemes)
        
        with open(os.path.join(currentDir, "audio", "separates", filename), "wb") as fp:
            fp.write(response)

        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "separates", filename)