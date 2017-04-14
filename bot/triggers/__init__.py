"""Custom triggers"""

from triggers.commands.sing import SingTrigger

def init_all_triggers(manager):
    """initialize all triggers"""
    SingTrigger().init_trigger(manager)
