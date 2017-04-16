"""Audio utilities"""

from pygame import mixer

def play(file, frequency=16000):
    """Play a MP3 file"""
    if mixer.get_init() is not None:
        mixer.quit()

    mixer.init(frequency=frequency)
    mixer.music.load(file)
    mixer.music.play()

def stop():
    """Stop currently playing audio"""
    mixer.init()
    mixer.music.stop()
