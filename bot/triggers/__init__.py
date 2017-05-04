"""Custom triggers"""

from triggers.commands import sing
from triggers.commands import say
from triggers.commands import stop
from triggers.commands import story
from triggers.inquire import base as inquire
from triggers.inquire import inquire_interest
from triggers.inquire import inquire_weather
from triggers.inquire import inquire_news
from triggers.inquire import inquire_entity
from triggers.misc import react
from triggers.misc import repeat
from triggers.admin import reload_conf

from ev3bot.trigger import register_trigger

def init_all_triggers(manager):
    """initialize all triggers"""
    register_trigger(manager, event_name='sing', action=sing.run)
    register_trigger(manager, event_name='say', action=say.run)
    register_trigger(manager, event_name='stop', action=stop.run)
    register_trigger(manager, event_name='tell_story',
                     action=story.run,
                     stop_action=story.stop_story)

    register_trigger(manager, event_name='react.*', action=react.run)
    register_trigger(manager, event_name='repeat', action=repeat.run)

    register_trigger(manager, event_name='inquire.entity.*', action=inquire_entity.run)
    register_trigger(manager, event_name='inquire.*', action=inquire.run)
    register_trigger(manager, event_name='inquire.interest', action=inquire_interest.run)
    register_trigger(manager, event_name='inquire.weather', action=inquire_weather.run)
    register_trigger(manager, event_name='inquire.news', action=inquire_news.run)

    register_trigger(manager, event_name='reload', action=reload_conf.run)
