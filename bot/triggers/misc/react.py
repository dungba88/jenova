"""Trigger implementation for reacting"""

from utils import tts

class React(object):
    """Trigger to react"""

    def run(self, execution_context, app_context):
        """run the action"""
        event_name = execution_context.event_name
        config_name = 'behavior.react.' + event_name.split('.')[1]
        reacts = app_context.get_config(config_name)
        if reacts is None or len(reacts) == 0:
            execution_context.finish('No react for ' + config_name)
            return

        tts.say_random_finish(reacts, execution_context)
