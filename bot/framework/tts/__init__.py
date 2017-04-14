"""Package for TTS support"""

from framework.tts.ev3 import EV3TTSEngine
from framework.tts.python import PyttsxEngine
from framework.tts.native import OSXTTSEngine

def say(engine_name, texts):
    """Speak texts with a specified engine"""
    tts_engines = {
        'pyttsx': PyttsxEngine(),
        'ev3': EV3TTSEngine(),
        'osx': OSXTTSEngine()
    }
    engine = tts_engines.get(engine_name)
    engine.say(texts)
