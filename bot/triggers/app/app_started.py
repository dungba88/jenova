"""Trigger implementation for inquiring entity info"""

import time

from ev3bot.trigger import Trigger

class AppStarted(Trigger):
    """Trigger to inquire information about an entity"""

    def run(self, execution_context):
        execution_context.finish()

        # notify by EV3 LED
        self.solid_green()

        # notify by Sound
        self.say_welcome(execution_context)

    def solid_green(self):
        """blink the LED green"""
        from ev3dev.ev3 import Leds
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set(Leds.LEFT, trigger='default-on')
        Leds.set(Leds.RIGHT, trigger='default-on')
        time.sleep(0.5)
        Leds.all_off()

    def say_welcome(self, execution_context):
        """say a welcome message"""
        song_id = self.app_context.get_config('behavior.app.started_song')
        execution_context.trigger_manager.fire('sing', {
            'song_id': song_id
        }, wait=False)
