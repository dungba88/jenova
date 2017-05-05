"""Custom triggers"""

from ev3bot.trigger import register_trigger
from triggers import teach
from triggers import train
from triggers import test
from triggers import predict
from triggers import say
from triggers import reload_conf

def init_all_triggers(manager):
    """initialize all triggers"""
    register_trigger(manager, event_name='teach', action=teach.run)
    register_trigger(manager, event_name='train', action=train.run)
    register_trigger(manager, event_name='test', action=test.run)
    register_trigger(manager, event_name='predict', action=predict.run)
    register_trigger(manager, event_name='say', action=say.run)
    register_trigger(manager, event_name='reload', action=reload_conf.run)
