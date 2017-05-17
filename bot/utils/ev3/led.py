"""module for LED control"""

import time
import logging

def solid_green():
    """blink the LED green"""
    try:
        from ev3dev.ev3 import Leds
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set(Leds.LEFT, trigger='default-on')
        Leds.set(Leds.RIGHT, trigger='default-on')
        time.sleep(0.5)
        Leds.all_off()
    except Exception as ex:
        logging.getLogger(__name__).error(str(ex))

def blink_green():
    """blink the LED green"""
    try:
        from ev3dev.ev3 import Leds
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set_color(Leds.RIGHT, Leds.GREEN)
        Leds.set(Leds.LEFT, brightness_pct=0.5, trigger='timer')
        Leds.set(Leds.RIGHT, brightness_pct=0.5, trigger='timer')
    except Exception as ex:
        logging.getLogger(__name__).error(str(ex))
