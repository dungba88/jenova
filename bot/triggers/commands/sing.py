"""Trigger implementation to sing"""

def sing_a_song(execution_context):
    """run the action"""
    print('Happy birthday to you')

def init_trigger(manager):
    """create and register the trigger"""
    trigger = manager.create_trigger(sing_a_song)
    manager.register_trigger('sing', trigger)
