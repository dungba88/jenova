"""TTS Engine by Python"""

import pyttsx

class PyttsxEngine(object):
    """Wrapper class for pyttsx"""
    def say(self, texts):
        """Speak the texts"""
        engine = pyttsx.init()
        for text in texts:
            engine.say(text)
        engine.runAndWait()
        