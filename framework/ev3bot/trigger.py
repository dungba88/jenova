"""Trigger framework"""

import re
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor

class TriggerExecutionContext(object):
    """The context a trigger can access whenever executed"""

    def __init__(self, event, event_name, trigger):
        self.event = event
        self.event_name = event_name
        self.trigger = trigger
        self.result = None
        self.exception = None
        self.finished = False
        self.rejected = False

    def finish(self, result=None):
        """mark execution as finished"""
        if self.finished or self.rejected:
            return
        self.result = result
        self.finished = True

    def reject(self, ex=None):
        """mark execution as rejected"""
        if self.finished or self.rejected:
            return
        self.exception = ex
        self.finished = True
        self.rejected = True

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
        self.error_handler = None
        self.timeout = 3

    def add_hook(self, name, handler):
        """Register a handler with an event name"""
        if name not in self.event_hook:
            self.event_hook[name] = list()
        self.event_hook[name].append(handler)

    def fire(self, name, event=None):
        """Fire the event, calling all handlers registered with the event"""
        handlers = self.get_handlers(name)
        if len(handlers) == 0:
            raise ValueError("Event. " + name + ". not registered")

        self.stop_all_actions()
        handler = handlers[random.randint(0, len(handlers) - 1)]
        execution_context = TriggerExecutionContext(event, name, None)
        self.executor.submit(handler, execution_context)
        start = time.time()
        while True:
            if execution_context.finished:
                if execution_context.exception is not None:
                    raise execution_context.exception # pylint: disable=E0702
                return execution_context.result
            if time.time() - start > self.timeout:
                break
            time.sleep(0.001)

    def get_handlers(self, name):
        """get all handlers registered for an event"""
        if name in self.event_hook:
            return self.event_hook[name]
        for registered_name in self.event_hook:
            if self.match(name, registered_name):
                return self.event_hook[registered_name]
        return []

    def match(self, name, registered_name):
        """check if the name matched a registered name"""
        return re.match(registered_name, name)

    def stop_all_actions(self):
        """stop all executing actions"""
        if self.current_trigger is not None:
            if self.current_trigger.stop_action is not None:
                self.current_trigger.stop_action()
        time.sleep(0.1)

    @classmethod
    def create_trigger(cls, action):
        """Create a trigger and associate with an action"""
        trigger = Trigger()
        trigger.action = action
        return trigger

    def register_trigger(self, name, trigger):
        """Register a trigger and run it"""
        self.triggers.append(trigger)

        def run_trigger(execution_context):
            """Run the closure trigger"""
            execution_context.trigger = trigger
            return self.run_trigger(execution_context)

        self.add_hook(name, run_trigger)

    def run_trigger(self, execution_context):
        """Run the trigger"""
        trigger = execution_context.trigger
        self.current_trigger = trigger

        try:
            if trigger.condition is not None:
                if not trigger.condition.satisfied_by(execution_context):
                    return

            return trigger.action(execution_context)
        except Exception as e:
            execution_context.reject(e)
            if self.error_handler is not None:
                self.error_handler.handle_error(e)
            else:
                logging.getLogger(__name__).error(e)

def register_trigger(manager, event_name, action, stop_action=None, condition=None):
    """create and register the trigger"""
    trigger = manager.create_trigger(action)
    trigger.condition = condition
    trigger.stop_action = stop_action
    manager.register_trigger(event_name, trigger)
