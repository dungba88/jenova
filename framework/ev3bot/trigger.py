"""Trigger framework"""

import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor

from ev3bot import audio

class TriggerExecutionContext(object):
    """The context a trigger can access whenever executed"""

    def __init__(self, event, event_name, trigger):
        self.event = event
        self.event_name = event_name
        self.trigger = trigger

class Trigger(object):
    """Represent a single Trigger"""

    def __init__(self):
        self.condition = None
        self.action = None
        self.stop_action = None

class TriggerManager(object):
    """Manage all triggers"""

    def __init__(self):
        self.triggers = list()
        self.event_hook = dict()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.current_trigger = None

    def add_hook(self, name, handler):
        """Register a handler with an event name"""
        if name not in self.event_hook:
            self.event_hook[name] = list()
        self.event_hook[name].append(handler)

    def fire(self, name, event=None):
        """Fire the event, calling all handlers registered with the event"""
        if name not in self.event_hook:
            raise ValueError("Event. " + name + ". not registered")

        self.stop_all_actions()
        handlers = self.event_hook[name]
        handler = handlers[random.randint(0, len(handlers) - 1)]
        self.executor.submit(handler, name, event)

    def stop_all_actions(self):
        """stop all executing actions"""
        if self.current_trigger is not None:
            if self.current_trigger.stop_action is not None:
                self.current_trigger.stop_action()
        time.sleep(0.1)
        audio.stop()

    @classmethod
    def create_trigger(cls, action):
        """Create a trigger and associate with an action"""
        trigger = Trigger()
        trigger.action = action
        return trigger

    def register_trigger(self, name, trigger):
        """Register a trigger and run it"""
        self.triggers.append(trigger)

        def run_trigger(name, event):
            """Run the closure trigger"""
            self.run_trigger(name, event, trigger)

        self.add_hook(name, run_trigger)

    def run_trigger(self, name, event, trigger):
        """Run the trigger"""
        self.current_trigger = trigger
        execution_context = TriggerExecutionContext(event, name, trigger)

        try:
            if trigger.condition is not None:
                if not trigger.condition.satisfied_by(execution_context):
                    return

            trigger.action(execution_context)
        except Exception as e:
            logging.getLogger(__name__).error(e)
