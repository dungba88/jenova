"""Trigger implementation for reacting"""

from ev3bot.trigger import Trigger

from utils import tts

class React(Trigger):
    """Trigger to react"""

    def run(self, execution_context):
        event_name = execution_context.event_name
        config_name = 'behavior.react.' + event_name.split('.')[1]
        reacts = self.get_config(config_name)
        if reacts is None or len(reacts) == 0:
            execution_context.finish('No react for ' + config_name)
            return

        tts.say_random_finish(reacts, execution_context)
