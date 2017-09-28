"""Trigger implementation to stop all actions"""

import time

class Stop(object):
    """Trigger to stop the action"""

    def run(self, execution_context, app_context):
        """run the action"""
        from utils.ev3 import tts, audio
        pause_time = app_context.get_config('behavior.stop.pause_time')
        stop_reacts = app_context.get_config('behavior.stop.reacts')
        execution_context.finish('stopping')

        audio.stop()
        time.sleep(pause_time)
        tts.say_random(stop_reacts)
