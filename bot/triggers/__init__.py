"""Custom triggers"""

from triggers.commands.sing import SingTrigger
from triggers.commands.say import SayTrigger

def init_all_triggers(manager):
    """initialize all triggers"""
    register_trigger(manager, event_name='sing', trigger=SingTrigger().run)
    register_trigger(manager, event_name='say', trigger=SayTrigger().run)

def register_trigger(manager, event_name, trigger):
    """create and register the trigger"""
    trigger = manager.create_trigger(trigger)
    manager.register_trigger(event_name, trigger)

