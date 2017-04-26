"""time facts"""

import time

def get_today():
    """get today"""
    return time.strftime("%x")

def get_time():
    """get current time"""
    return time.strftime("%X")

def get_day():
    """get today's day"""
    return time.strftime("%A")
