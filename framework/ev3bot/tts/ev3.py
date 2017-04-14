"""TTS Engine by EV3"""

from ev3dev import ev3

class EV3TTSEngine(object):
    """Wrapper class for EV3 TTS"""
    def say(self, texts):
        """Speak the texts"""
        for text in texts:
            ev3.Sound.speak(text)
            