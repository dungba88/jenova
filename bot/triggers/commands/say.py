"""Trigger implementation to say"""

from utils import tts

class SayTrigger(object):
    """Trigger class for say a paragraph"""

    def run(self, execution_context):
        """run the action"""
        text = execution_context.event.get('text', None)

        if text is not None:
            tts.say([text])
            