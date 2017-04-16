"""Trigger implementation to stop all actions"""

import time
import random

from app import APP_INSTANCE as app
from utils import tts

def run(execution_context):
    """run the action"""
    pause_time = app.get_config('behavior.stop.pause_time')
    stop_reacts = app.get_config('behavior.stop.reacts')
    time.sleep(pause_time)
    react = stop_reacts[random.randint(0, len(stop_reacts) - 1)]
    tts.say([react])
