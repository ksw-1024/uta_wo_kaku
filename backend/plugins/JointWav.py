import os
import shutil

from pydub import AudioSegment

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

def joint_audio(inputs, output):
    print(inputs)
    l = len(inputs)
    print(l)
    i = 0
    while (i < (l - 1)):
        print(str(i+1) + "番目の処理を開始")
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
    
    #Sepatateファイルの中身を削除
    if(os.path.isdir(os.path.join(currentDir, "audio", "separates"))):
        print("ファイルの削除を実行します")
        shutil.rmtree(os.path.join(currentDir, "audio", "separates"))
        print("ディレクトリの復元を実行します")
        os.mkdir(os.path.join(currentDir, "audio", "separates"))