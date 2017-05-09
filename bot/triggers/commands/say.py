"""Trigger implementation to say"""

from ev3bot.trigger import Trigger

from utils import tts

class Say(Trigger):
    """Trigger to speak a text"""

    def run(self, execution_context):
        text = execution_context.event.get('text', None)
        execution_context.finish(text)

        if text is not None:
            tts.say([text])
