"""Trigger implementation for repeating last sentence"""

from utils import tts

class Repeat(object):
    """Trigger to repeat last words"""

    def run(self, execution_context, _):
        """run the action"""
        execution_context.finish(tts.LAST_SENTENCE)
        if tts.LAST_SENTENCE is not None:
            tts.say(tts.LAST_SENTENCE)
