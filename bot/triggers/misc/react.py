"""Trigger implementation for reacting"""

from app import APP_INSTANCE as app
from utils import tts

def run(execution_context):
    """run the action"""
    event_name = execution_context.event_name
    config_name = 'behavior.react.' + event_name.split('.')[1]
    reacts = app.get_config(config_name)
    if reacts is None or len(reacts) == 0:
        execution_context.finish('No react')
        return

    execution_context.finish()
    tts.say_random(reacts)
