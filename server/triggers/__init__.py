"""Custom triggers"""

from ev3bot.trigger import register_trigger
from triggers.add_input import run as add_input
from triggers.train import run as train
from triggers.test import run as test

def init_all_triggers(manager):
    """initialize all triggers"""
    register_trigger(manager, event_name='add_input', action=add_input)
    register_trigger(manager, event_name='train', action=train)
    register_trigger(manager, event_name='test', action=test)
