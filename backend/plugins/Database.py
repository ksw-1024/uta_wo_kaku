import os
import random, string

import sqlite3

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

def data_push(filename, sepatate_filename, word):
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3","AUDIO_DATA.db"))
    
    cur = conn.cursor()  # カーソルを作成
    
    cur.execute('CREATE TABLE IF NOT EXISTS audio(id INTEGER PRIMARY KEY AUTOINCREMENT,time TIMESTAMP, filename STRING, separate_filename STRING, word STRING)')  # tableを作成する指示
    cur.execute('INSERT INTO audio(time, filename, separate_filename, word) VALUES(CURRENT_TIMESTAMP, "{}", "{}", "{}")'.format(filename, sepatate_filename, word))
    
    conn.commit()
    
    conn.close()
    
def delete_table():
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3","AUDIO_DATA.db"))
    
    cur = conn.cursor()  # カーソルを作成
    cur.execute('CREATE TABLE IF NOT EXISTS audio(id INTEGER PRIMARY KEY AUTOINCREMENT,time TIMESTAMP, filename STRING, separate_filename STRING, word STRING)')
    cur.execute('DROP TABLE audio')
    
    conn.commit()
    conn.close()
    
def get_info(filename):
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3","AUDIO_DATA.db"))
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM audio WHERE filename="{}"'.format(filename))
    word_data = cur.fetchall()
    
    conn.close()
    return word_data
    
if __name__ == '__main__':
    delete_table()