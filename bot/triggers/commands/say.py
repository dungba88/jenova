"""Trigger implementation to say"""

from utils import tts

class Say(object):
    """Trigger to speak a text"""

    def run(self, execution_context, _):
        """run the action"""
        text = execution_context.event.get('text', None)
        execution_context.finish(text)

        if text is not None:
            tts.say([text])
