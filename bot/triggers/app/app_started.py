"""Trigger implementation for inquiring entity info"""

from ev3bot.trigger import Trigger
from utils.ev3 import led

class AppStarted(Trigger):
    """Trigger to inquire information about an entity"""

    def run(self, execution_context):
        execution_context.finish()

        # notify by EV3 LED
        led.solid_green()

        # notify by Sound
        self.say_welcome(execution_context)

    def say_welcome(self, execution_context):
        """say a welcome message"""
        song_id = self.app_context.get_config('behavior.app.started_song')
        execution_context.trigger_manager.fire('sing', {
            'song_id': song_id
        }, wait=False)
