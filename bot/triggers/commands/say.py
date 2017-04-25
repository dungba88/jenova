"""Trigger implementation to say"""

from utils import tts

def run(execution_context):
    """run the action"""
    text = execution_context.event.get('text', None)
    execution_context.finish(text)

    if text is not None:
        tts.say([text])
