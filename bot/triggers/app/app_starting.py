"""Trigger implementation for inquiring entity info"""

from ev3bot.trigger import Trigger

from utils.ev3 import led

class AppStarting(Trigger):
    """Trigger to inquire information about an entity"""

    def run(self, execution_context):
        execution_context.finish()

        # notify by EV3 LED
        led.blink_green()
