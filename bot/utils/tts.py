"""TTS utility"""

import logging

from app import APP_INSTANCE as app

from ev3bot.tts import PyttsxEngine
from ev3bot.tts import GTTSEngine
from ev3bot.tts import EV3TTSEngine
from ev3bot.tts import OSXTTSEngine

def say(engine_name, texts):
    """Speak texts with a specified engine"""
    osx_voice = app.get_config('engine.voices.osx')
    gtts_lang = app.get_config('engine.lang')

    tts_engines = {
        'pyttsx': PyttsxEngine(),
        'gTTS': GTTSEngine(gtts_lang),
        'ev3': EV3TTSEngine(),
        'osx': OSXTTSEngine(osx_voice)
    }
    engine = tts_engines.get(engine_name)
    if engine is None:
        logging.warning('engine not configured: ' + engine_name)
        return
    engine.say(texts)
