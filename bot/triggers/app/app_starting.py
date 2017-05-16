"""Trigger implementation for inquiring entity info"""

from ev3bot.trigger import Trigger

class AppStarting(Trigger):
    """Trigger to inquire information about an entity"""

    def run(self, execution_context):
        execution_context.finish()

        # notify by EV3 LED
        self.blink_green()

    def blink_green(self):
        """blink the LED green"""
        from ev3dev.ev3 import Leds
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set_color(Leds.RIGHT, Leds.GREEN)
        Leds.set(Leds.LEFT, brightness_pct=0.5, trigger='timer')
        Leds.set(Leds.RIGHT, brightness_pct=0.5, trigger='timer')
