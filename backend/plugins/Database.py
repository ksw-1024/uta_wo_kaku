import os

import sqlite3

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

def data_push():
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3","AUDIO_DATA.db"))
    
    cur = conn.cursor()  # カーソルを作成
    cur.execute('CREATE TABLE IF NOT EXISTS audio(id INTEGER PRIMARY KEY AUTOINCREMENT,time TIMESTAMP, filename STRING, word STRING)')  # tableを作成する指示
    #cur.execute('INSERT INTO audio(time, filename, word) VALUES(CURRENT_TIMESTAMP, "filename.wav", "てにほは")')
    
    conn.commit()  # commit()した時点でDBファイルが更新されます
    
    cur.execute('SELECT * FROM audio WHERE filename="filename.wav"')
    
    word_data = cur.fetchall()
    
    print(word_data)
    
    conn.close()
    
if __name__ == '__main__':
    data_push()