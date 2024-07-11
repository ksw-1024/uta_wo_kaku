from pydub import AudioSegment

sound1 = AudioSegment.from_file("/Users/wxwxw/Documents/uta_wo_kaku/backend/audio/20240711203723549692.wav")
sound2 = AudioSegment.from_file("/Users/wxwxw/Documents/uta_wo_kaku/backend/audio/20240711203728795926.wav")

output = sound1.overlay(sound2, position=0)

# save the result
output.export("/Users/wxwxw/Documents/uta_wo_kaku/backend/audio/20240711203728795926.wav", format="wav")