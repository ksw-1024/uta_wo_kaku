import os
import xml.etree.ElementTree as ET

from plugins.Wakachigaki import to_kana
#from Wakachigaki import to_kana

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

xmlfilepath: str = os.path.join(currentDir, "setting", "housouKinshiYougo.xml")
tree = ET.parse(xmlfilepath)

root = tree.getroot()
child = root.findall("dirtyWord")


NGWord: list = []
NG_Hira: list = []
NG_Kana: list = []

for c in child:
    main_word = c.find("word")
    
    NGWord.append(main_word.text)
    NG_Hira.append(str(main_word.attrib["reading"]))
    NG_Kana.append(to_kana(str(main_word.attrib["reading"])))
    
    grandchild = c.find("replaceWordList")
    replaces = grandchild.findall("word")
    for r in replaces:
        NGWord.append(r.text)
        NG_Hira.append(str(r.attrib["reading"]))
        NG_Kana.append(to_kana(str(r.attrib["reading"])))
    
def is_ng(word: str):
    for index, ng in enumerate(NGWord):
        if(word in ng or ng in word):
            return True
        elif(word in NG_Hira[index] or NG_Hira[index] in word):
            return True
        elif(word in NG_Kana[index] or NG_Kana[index] in word):
            return True
        
    return False
