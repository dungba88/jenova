"""Trigger implementation to say"""

import app
from framework import tts

class SayTrigger(object):
    """Trigger class for say a paragraph"""

    def init_trigger(self, manager):
        """create and register the trigger"""
        trigger = manager.create_trigger(self.say)
        manager.register_trigger('say', trigger)

    def say(self, execution_context):
        """run the action"""
        text = execution_context.event.get('text', None)

        if text is not None:
            tts_engine_name = app.get_config('engine').get('tts_engine')
            tts.say(tts_engine_name, [text])
