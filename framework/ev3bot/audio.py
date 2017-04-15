"""Audio utilities"""

from pygame import mixer

def play(file, frequency=16000):
    """Play a MP3 file"""
    mixer.init(frequency=frequency)
    mixer.music.load(file)
    mixer.music.play()
