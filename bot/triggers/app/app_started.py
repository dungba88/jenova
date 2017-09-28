"""Trigger implementation for inquiring entity info"""

from utils.ev3 import led

class AppStarted(object):
    """Trigger to inquire information about an entity"""

    def run(self, execution_context, app_context):
        """run the action"""
        execution_context.finish()

        # notify by EV3 LED
        led.solid_green()

        # notify by Sound
        self.say_welcome(execution_context, app_context)

    def say_welcome(self, execution_context, app_context):
        """say a welcome message"""
        song_id = app_context.get_config('behavior.app.started_song')
        execution_context.trigger_manager.fire('sing', {
            'song_id': song_id
        }, wait=False)
