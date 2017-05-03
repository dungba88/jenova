"""Trigger implementation for repeating last sentence"""

from utils import tts

def run(execution_context):
    """run the action"""
    execution_context.finish(tts.LAST_SENTENCE)
    if tts.LAST_SENTENCE is not None:
        tts.say(tts.LAST_SENTENCE)
