import os
import json

import re
from pykakasi import kakasi

from logging import getLogger, config

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

#ログの準備
with open(os.path.join(currentDir, "setting", "log_config.json"), 'r') as f:
    log_conf = json.load(f)

config.dictConfig(log_conf)
logger = getLogger(__name__)

c1 = '[ウクスツヌフムユルグズヅブプヴ][ァィェォ]' #ウ段＋「ァ/ィ/ェ/ォ」
c2 = '[イキシチニヒミリギジヂビピ][ャュェョ]' #イ段（「イ」を除く）＋「ャ/ュ/ェ/ョ」
c3 = '[テデ][ィュ]' #「テ/デ」＋「ャ/ィ/ュ/ョ」
c4 = '[ァ-ヴー]' #カタカナ１文字（長音含む）

cond = '('+c1+'|'+c2+'|'+c3+'|'+c4+')'
re_mora = re.compile(cond)

<<<<<<< HEAD:backend/plugins/Wakachigaki.py
def moraWakachi(kana_text):
    return re_mora.findall(kana_text)
=======
kks = kakasi()

def moraWakachi(text: str) -> int:
    kana_text = ""
    result = kks.convert(text)
    for converted_word in result:
        kana_text = kana_text + converted_word["kana"]
        
    logger.info(f"Results of the share and write : {re_mora.findall(kana_text)}")
    return len(re_mora.findall(kana_text))
>>>>>>> backend_dev:backend/plugins/wakachigaki.py
