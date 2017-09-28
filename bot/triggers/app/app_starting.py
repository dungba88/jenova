"""Trigger implementation for inquiring entity info"""

from utils.ev3 import led

class AppStarting(object):
    """Trigger to inquire information about an entity"""

    def run(self, execution_context, _):
        """run the action"""
        execution_context.finish()

        # notify by EV3 LED
        led.blink_green()
