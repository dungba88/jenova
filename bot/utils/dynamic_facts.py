"""dynamic facts"""

import time
import random

from app import APP_INSTANCE as app

def get_battery_level():
    """get battery level"""
    from ev3dev.core import PowerSupply
    supply = PowerSupply()
    return supply.measured_voltage / supply.max_voltage * 100

def get_health_react():
    """get health react"""
    health = app.get_config('facts.health')
    reacts = app.get_config('behavior.health_react.' + health)
    return reacts[random.randint(0, len(reacts) - 1)]

def get_today():
    """get today"""
    return time.strftime("%x")

def get_time():
    """get current time"""
    return time.strftime("%X")

def get_day():
    """get today's day"""
    return time.strftime("%A")
