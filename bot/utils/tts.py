"""TTS utility"""

import logging
import random
import re

from app import APP_INSTANCE as app
from utils import dynamic_facts

from ev3bot.tts import PyttsxEngine
from ev3bot.tts import GTTSEngine
from ev3bot.tts import EV3TTSEngine
from ev3bot.tts import OSXTTSEngine
from ev3bot.tts import MaryTTS

REGEX = re.compile(r'\{([^\}]*)\}')

def say_random(texts, params=None):
    """Speak a random text from a list"""
    if texts is None:
        return
    text = texts[random.randint(0, len(texts) - 1)]
    say([text], params)

def say(texts, params=None):
    """Speak texts with a specified engine"""
    if texts is None:
        return
    texts = normalize(texts, params)

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

def normalize(texts, params):
    """normalize texts"""
    return list(map(lambda text: normalize_text(text, params), texts))

def normalize_text(text, params):
    """normalize a single text"""
    groups = REGEX.findall(text)
    for group in groups:
        fact = None
        if params is not None and group in params:
            fact = params[group]
        if fact is None:
            fact = get_fact(group)
            if isinstance(fact, list):
                fact = fact[random.randint(0, len(fact) - 1)]
        text = text.replace('{' + group + '}', str(fact))
    return text

def get_fact(group):
    """get fact by name"""
    facts = app.get_config('facts')
    fact = facts.get(group)
    if fact is not None:
        return fact
    method = getattr(dynamic_facts, 'get_' + group, None)
    if method is None:
        return "unknown"
    return method()
