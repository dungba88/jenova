"""TTS Engine by Python"""

from tempfile import NamedTemporaryFile
from ev3bot import audio

class PyttsxEngine(object):
    """Wrapper class for pyttsx"""
    def say(self, texts):
        """Speak the texts"""
        import pyttsx
        engine = pyttsx.init()
        for text in texts:
            engine.say(text)
        engine.runAndWait()

class GTTSEngine(object):
    """Wrapper class for gTTS"""
    def __init__(self, lang):
        self.lang = lang

    def say(self, texts):
        """Speak the texts"""
        for text in texts:
            self.speak_text(text)

    def speak_text(self, text):
        """Speak a single text"""
        from gtts import gTTS
        tts = gTTS(text=text, lang=self.lang)
        # save the speech to temp file
        tmp_file = NamedTemporaryFile()
        tts.write_to_fp(tmp_file)
        # play it with pyaudio
        audio.play(tmp_file.name)
        # remove it
        tmp_file.close()
