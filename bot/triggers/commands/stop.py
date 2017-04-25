"""Trigger implementation to stop all actions"""

import time

from app import APP_INSTANCE as app
from utils import tts
from ev3bot import audio

def run(execution_context):
    """run the action"""
    pause_time = app.get_config('behavior.stop.pause_time')
    stop_reacts = app.get_config('behavior.stop.reacts')
    execution_context.finish('stopping')

    audio.stop()
    time.sleep(pause_time)
    tts.say_random(stop_reacts)
