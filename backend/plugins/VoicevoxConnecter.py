import os, sys

from pathlib import Path
from voicevox_core import VoicevoxCore, METAS

currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

core = VoicevoxCore(open_jtalk_dict_dir=os.path.join(currentDir, "open_jtalk_dic_utf_8-1.11"))

#各種値を定義
speed_scale = 1.6
pitch_scale = 0.06
pre_phoneme_length = 0

def render_voice(text: str, speaker_id = 1):
    if not core.is_model_loaded(speaker_id):
        core.load_model(speaker_id)
        
    audio_query = core.audio_query(text, speaker_id)
        
    audio_query.speed_scale = speed_scale
    audio_query.pitch_scale = pitch_scale
    audio_query.pre_phoneme_length = pre_phoneme_length
        
    wave_bytes = core.synthesis(audio_query, speaker_id)
        
    return wave_bytes