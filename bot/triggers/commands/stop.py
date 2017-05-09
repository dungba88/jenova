"""Trigger implementation to stop all actions"""

import time

from ev3bot import audio
from ev3bot.trigger import Trigger

from utils import tts

class Stop(Trigger):
    """Trigger to stop the action"""

    def run(self, execution_context):
        pause_time = self.get_config('behavior.stop.pause_time')
        stop_reacts = self.get_config('behavior.stop.reacts')
        execution_context.finish('stopping')

        audio.stop()
        time.sleep(pause_time)
        tts.say_random(stop_reacts)
