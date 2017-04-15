"""TTS utility"""

import logging

from app import APP_INSTANCE as app

from ev3bot.tts import PyttsxEngine
from ev3bot.tts import GTTSEngine
from ev3bot.tts import EV3TTSEngine
from ev3bot.tts import OSXTTSEngine
from ev3bot.tts import MaryTTS

def say(texts):
    """Speak texts with a specified engine"""
    engine_name = app.get_config('engine.tts.engine')
    osx_voice = app.get_config('engine.tts.osx.voice')
    gtts_lang = app.get_config('engine.tts.gTTS.lang')
    mary_config = app.get_config('engine.tts.mary_tts')

    tts_engines = {
        'pyttsx': PyttsxEngine(),
        'gTTS': GTTSEngine(gtts_lang),
        'ev3': EV3TTSEngine(),
        'osx': OSXTTSEngine(osx_voice),
        'mary_tts': MaryTTS(mary_config)
    }
    engine = tts_engines.get(engine_name)
    if engine is None:
        logging.warning('engine not configured: ' + engine_name)
        return
    engine.say(texts)
