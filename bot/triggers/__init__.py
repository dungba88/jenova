"""Custom triggers"""

from triggers.commands.sing import SingTrigger
from triggers.commands.say import SayTrigger

def init_all_triggers(manager):
    """initialize all triggers"""
    SingTrigger().init_trigger(manager)
    SayTrigger().init_trigger(manager)
