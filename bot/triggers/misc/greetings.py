"""Trigger implementation for greeting"""

import random

from app import APP_INSTANCE as app
from utils import tts

def run(execution_context):
    """run the action"""
    greetings_reacts = app.get_config('behavior.greetings.reacts')
    react = greetings_reacts[random.randint(0, len(greetings_reacts) - 1)]
    tts.say([react])
    