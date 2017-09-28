"""Audio utilities"""

import time

def play(file, frequency=16000):
    """Play a MP3 file"""
    from pygame import mixer

    if mixer.get_init() is not None:
        mixer.quit()

    mixer.init(frequency=frequency)
    mixer.music.load(file)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.1)

def stop():
    """Stop currently playing audio"""
    from pygame import mixer

    mixer.init()
    mixer.music.stop()
