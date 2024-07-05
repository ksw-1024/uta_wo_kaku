import json
import requests
import simpleaudio as sa
import io
import wave

def generate_and_play_wav(text, speaker=1):
    host = 'localhost'
    port = 50021
    params = (
        ('text', text),
        ('speaker', speaker),
    )

    # 音声合成のためのクエリを送信
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )

    headers = {'Content-Type': 'application/json',}

    # 合成された音声データを取得
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    # バイナリデータをwaveオブジェクトとして読み込む
    with io.BytesIO(response2.content) as audio_io:
        with wave.open(audio_io, 'rb') as wave_read:
            # simpleaudioで再生可能なオーディオオブジェクトを生成
            audio_data = wave_read.readframes(wave_read.getnframes())
            wave_obj = sa.WaveObject(audio_data, wave_read.getnchannels(), wave_read.getsampwidth(), wave_read.getframerate())

    # WAVファイル再生部分
    play_obj = wave_obj.play()
    play_obj.wait_done()  # 再生が完了するまで待つ

if __name__ == '__main__':
    text = '明日の天気は晴れと雪だよ'
    generate_and_play_wav(text)