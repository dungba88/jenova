"""Custom triggers"""

from triggers.commands.sing import run as sing
from triggers.commands.say import run as say
from triggers.commands.stop import run as stop
from triggers.commands.story import run as story
from triggers.commands.story import stop_story as stop_story
from triggers.misc.react import run as react
from ev3bot.trigger import register_trigger

def init_all_triggers(manager):
    """initialize all triggers"""
    register_trigger(manager, event_name='sing', action=sing)
    register_trigger(manager, event_name='say', action=say)
    register_trigger(manager, event_name='stop', action=stop)
    register_trigger(manager, event_name='greetings', action=react)
    register_trigger(manager, event_name='thank', action=react)
    register_trigger(manager, event_name='inquire.story', action=story, stop_action=stop_story)
