"""Native TTS engine"""

from os import system

class OSXTTSEngine(object):
    """Wrapper class for OSX native TTS"""
    def say(self, texts):
        """Speak the texts"""
        for text in texts:
            # speak with Stephen Hawking-like voice :D
            system('say -v Fred ' + text)
