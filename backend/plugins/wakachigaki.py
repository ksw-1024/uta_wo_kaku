import re

c1 = '[ウクスツヌフムユルグズヅブプヴ][ァィェォ]' #ウ段＋「ァ/ィ/ェ/ォ」
c2 = '[イキシチニヒミリギジヂビピ][ャュェョ]' #イ段（「イ」を除く）＋「ャ/ュ/ェ/ョ」
c3 = '[テデ][ィュ]' #「テ/デ」＋「ャ/ィ/ュ/ョ」
c4 = '[ァ-ヴー]' #カタカナ１文字（長音含む）

cond = '('+c1+'|'+c2+'|'+c3+'|'+c4+')'
re_mora = re.compile(cond)

def moraWakachi(kana_text):
    return re_mora.findall(kana_text)