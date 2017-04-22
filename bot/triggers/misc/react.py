"""Trigger implementation for greeting"""

from app import APP_INSTANCE as app
from utils import tts

def run(execution_context):
    """run the action"""
    config_name = 'behavior.react.' + execution_context.event_name
    reacts = app.get_config(config_name)
    tts.say_random(reacts)
