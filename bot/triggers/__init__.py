"""Custom triggers"""

from triggers.commands.sing import run as sing
from triggers.commands.say import run as say
from triggers.commands.stop import run as stop
from triggers.misc.greetings import run as greetings

def init_all_triggers(manager):
    """initialize all triggers"""
    register_trigger(manager, event_name='sing', action=sing)
    register_trigger(manager, event_name='say', action=say)
    register_trigger(manager, event_name='stop', action=stop)
    register_trigger(manager, event_name='greetings', action=greetings)

def register_trigger(manager, event_name, action, stop_action=None, condition=None):
    """create and register the trigger"""
    trigger = manager.create_trigger(action)
    trigger.condition = condition
    trigger.stop_action = stop_action
    manager.register_trigger(event_name, trigger)

