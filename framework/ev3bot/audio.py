"""Audio utilities"""

from pygame import mixer

def play(file):
    """Play a MP3 file"""
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()
