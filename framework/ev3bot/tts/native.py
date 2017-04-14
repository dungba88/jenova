"""Native TTS engine"""

from os import system

class OSXTTSEngine(object):
    """Wrapper class for OSX native TTS"""

    def __init__(self, voice):
        self.voice = voice

    def say(self, texts):
        """Speak the texts"""
        for text in texts:
            system('say -v ' + self.voice + ' ' + text)
