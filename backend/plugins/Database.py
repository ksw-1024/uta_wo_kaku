import os
import random, string

import sqlite3

import datetime

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
conn = sqlite3.connect(os.path.join(currentDir, "SQLite3","AUDIO_DATA.db"))

cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS audio(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP, filename STRING, separate_filename STRING, word STRING)')
cur.execute('CREATE TABLE IF NOT EXISTS temp_audio(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP, filename STRING, filepath STRING, word STRING, onnso INTEGER)')
cur.execute('CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP, filename STRING, word STRING)')


conn.commit()
conn.close()

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

def data_push(filename, sepatate_filename, word):
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3","AUDIO_DATA.db"))
    
    cur = conn.cursor()  # カーソルを作成
    
    cur.execute('CREATE TABLE IF NOT EXISTS audio(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP, filename STRING, separate_filename STRING, word STRING)')
    cur.execute('INSERT INTO audio(time, filename, separate_filename, word) VALUES(CURRENT_TIMESTAMP, "{}", "{}", "{}")'.format(filename, sepatate_filename, word))
    
    conn.commit()
    
    conn.close()
    
def temp_data_push(separate_filename: str, filepath: str, word: str, onnso: int):
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3", "AUDIO_DATA.db"))
    
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS temp_audio(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP, filename STRING, filepath STRING, word STRING, onnso INTEGER)')
    cur.execute('INSERT INTO temp_audio(time, filename, filepath, word, onnso) VALUES (CURRENT_TIMESTAMP, "{}", "{}", "{}", {})'.format(separate_filename, filepath, word, onnso))
    
    conn.commit()
    
    conn.close()

def history_data_push(filename: str, word: str):
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3", "AUDIO_DATA.db"))
    
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP, filename STRING, word STRING)')
    cur.execute('INSERT INTO history(time, filename, word) VALUES (CURRENT_TIMESTAMP, "{}", "{}")'.format(filename, word))
    
    conn.commit()
    
    conn.close()
    
def delete_table(table_name: str):
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3","AUDIO_DATA.db"))
    
    cur = conn.cursor()  # カーソルを作成
    cur.execute('CREATE TABLE IF NOT EXISTS {}(id INTEGER PRIMARY KEY AUTOINCREMENT,time TIMESTAMP, filename STRING, separate_filename STRING, word STRING)'.format(table_name))
    cur.execute('DROP TABLE {}'.format(table_name))
    
    conn.commit()
    conn.close()
    
def get_info_row(table: str, category: str, key: str):
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3","AUDIO_DATA.db"))
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM {} WHERE {}="{}"'.format(table, category, key))
    word_data = cur.fetchall()
    
    conn.close()
    return word_data

def get_info_column(column_name: str, table: str) -> list:
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3", "AUDIO_DATA.db"))
    cur = conn.cursor()
    
    cur.execute(f'SELECT {column_name} FROM {table}')
    data = cur.fetchall()
    
    conn.close()
    return data

def get_info_latest(table: str):
    conn = sqlite3.connect(os.path.join(currentDir, "SQLite3", "AUDIO_DATA.db"))
    cur = conn.cursor()
    
    latest_data = cur.execute(f"SELECT max(rowid), * FROM {table}").fetchall()
    
    return latest_data

def all_reset_table():
    delete_table("audio")
    delete_table("temp_audio")
    delete_table("history")
    
if __name__ == '__main__':
    all_reset_table()