import os, sys

from pathlib import Path
from voicevox_core import VoicevoxCore, METAS

def test():
    currentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    return currentDir