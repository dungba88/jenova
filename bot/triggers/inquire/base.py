"""Trigger implementation for inquiring"""

import logging

from app import APP_INSTANCE as app
from utils import tts

LOGGER = logging.getLogger(__name__)

def run(execution_context):
    """run the action"""
    event_name = execution_context.event_name.split('.')[1]
    config_name = 'behavior.inquire.' + event_name
    reacts = app.get_config(config_name)
    txt_no_data = app.get_config('behavior.inquire.no_data')
    if reacts is None or len(reacts) == 0:
        LOGGER.warning('No behavior configured for ' + config_name)
        tts.say_random_finish(txt_no_data, execution_context)
        return
    tts.say_random_finish(reacts, execution_context)
