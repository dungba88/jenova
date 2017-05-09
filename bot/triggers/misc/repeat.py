"""Trigger implementation for repeating last sentence"""

from ev3bot.trigger import Trigger

from utils import tts

class Repeat(Trigger):
    """Trigger to repeat last words"""

    def run(self, execution_context):
        execution_context.finish(tts.LAST_SENTENCE)
        if tts.LAST_SENTENCE is not None:
            tts.say(tts.LAST_SENTENCE)
