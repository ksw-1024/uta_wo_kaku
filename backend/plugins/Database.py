import os
import random, string

import sqlite3

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

def data_push():
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3","AUDIO_DATA.db"))
    
    cur = conn.cursor()  # カーソルを作成
    cur.execute('DROP TABLE audio')
    
    cur.execute('CREATE TABLE IF NOT EXISTS audio(id INTEGER PRIMARY KEY AUTOINCREMENT,time TIMESTAMP, sepatate_filename STRING, word STRING, filename STRING)')  # tableを作成する指示
    #cur.execute('INSERT INTO audio(time, filename, word) VALUES(CURRENT_TIMESTAMP, "filename.wav", "てにほは")')
    
    conn.commit()  # commit()した時点でDBファイルが更新されます
    
    cur.execute("SELECT name from sqlite_master where type='table';")
    print('table一覧: ', cur.fetchall())
    
    #cur.execute('SELECT * FROM audio WHERE filename="filename.wav"')
    #word_data = cur.fetchall()
    
    #print(word_data)
    
    conn.close()
    
if __name__ == '__main__':
    data_push()