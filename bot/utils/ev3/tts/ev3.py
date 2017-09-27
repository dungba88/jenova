"""TTS Engine by EV3"""

class EV3TTSEngine(object):
    """Wrapper class for EV3 TTS"""
    def say(self, texts):
        """Speak the texts"""
        from ev3dev import ev3
        for text in texts:
            ev3.Sound.speak(text).wait()
