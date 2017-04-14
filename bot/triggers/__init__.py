"""Custom triggers"""

from triggers.commands import sing

def init_all_triggers(manager):
    """initialize all triggers"""
    sing.init_trigger(manager)
