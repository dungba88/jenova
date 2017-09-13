"""Trigger framework"""

import re
import time
import logging
import threading
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

class TriggerExecutionStatus(Enum):
    """Represent the status of the execution"""
    CREATED = 1
    EXECUTING = 2
    FINISHED = 3
    REJECTED = 4

class TriggerExecutionContext(object):
    """The context a trigger can access whenever executed"""

    def __init__(self, event, event_name, trigger):
        self.event = event
        self.event_name = event_name
        self.trigger = trigger
        self.trigger_manager = None
        self.result = None
        self.exception = None
        self.status = TriggerExecutionStatus.CREATED
        self.lock = threading.Lock()

    def start_lock(self):
        """start locking the context"""
        self.lock.acquire(blocking=False)

    def acquire_lock(self, timeout=-1):
        """start locking the context"""
        self.lock.acquire(timeout=timeout)

    def is_completed(self):
        """check if the execution is completed, whether finished successfully or failed"""
        return self.status == TriggerExecutionStatus.FINISHED \
                or self.status == TriggerExecutionStatus.REJECTED

    def finish(self, result=None):
        """mark execution as finished"""
        if self.is_completed():
            return
        self.result = result
        self.status = TriggerExecutionStatus.FINISHED
        self.lock.release()

    def reject(self, ex=None):
        """mark execution as rejected"""
        if self.is_completed():
            return
        self.exception = ex
        self.status = TriggerExecutionStatus.REJECTED
        self.lock.release()

class TriggerCondition(object):
    """Represent a trigger condition"""

    def __init__(self, predicate):
        from pypred import Predicate
        self.predicate = Predicate(predicate)
        if not self.predicate.is_valid():
            raise ValueError('Predicate is invalid: ' + str(predicate))

    def satisfied_by(self, execution_context):
        """test the predicate against the execution context"""
        return self.predicate.evaluate(execution_context)

class TriggerConfig(object):
    """Represent a Trigger configuration"""

    def __init__(self):
        self.condition = None
        self.stop_all_actions = False
        self.trigger = None

    def check_condition(self, execution_context):
        """check if the condition is satisfied"""
        if self.condition is None:
            return True
        return self.condition.satisfied_by(execution_context):

    def check_stop_all_actions(self, execution_context):
        """check if the condition of stop_all_actions is satisfied"""
        if self.stop_all_actions is None:
            return False
        if isinstance(self.stop_all_actions, bool):
            return self.stop_all_actions
        if isinstance(self.stop_all_actions, str):
            condition = TriggerCondition(self.stop_all_actions)
            return condition.satisfied_by(execution_context)
        return False

class TriggerManager(object):
    """Manage all triggers"""

    def __init__(self):
        self.triggers = list()
        self.event_hook = dict()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.current_trigger = None
        self.error_handler = None
        self.timeout = 3
        self.app_context = None
        self.stop_hooks = list()

    def add_stop_hook(self, handler):
        """Register a handler for when trigger needs to be stopped"""
        self.stop_hooks.append(handler)

    def add_hook(self, name, handler):
        """Register a handler with an event name"""
        if name not in self.event_hook:
            self.event_hook[name] = list()
        self.event_hook[name].append(handler)

    def remove_all(self):
        """Remove all trigger"""
        self.stop_all_actions()
        self.triggers = list()
        self.event_hook = dict()

    def fire(self, name, event=None, wait=True):
        """Fire the event, calling all handlers registered with the event"""
        trigger_configs = self.get_handlers(name)
        if len(trigger_configs) == 0:
            logging.getLogger(__name__).warning("Event. " + name + ". not registered")
            return

        execution_context = TriggerExecutionContext(event, name, None)
        trigger_configs = self.get_matching_triggers(trigger_configs, execution_context)
        if len(trigger_configs) == 0:
            return

        if self.is_eligible_for_stop(trigger_configs, execution_context):
            self.stop_all_actions()

        result = None
        for config in trigger_configs:
            # build the execution context
            execution_context = TriggerExecutionContext(event, name, None)
            execution_context.trigger = config.trigger
            execution_context.trigger_manager = self

            if wait:
                self.executor.submit(self.run_trigger, execution_context)
            else:
                result = self.run_trigger(execution_context)

        if not wait:
            return result
        return self.wait_for_finish(execution_context)

    def is_eligible_for_stop(self, triggers, execution_context):
        """check if any of the triggers is eligible to stop all actions"""
        for trigger in triggers:
            if trigger.check_stop_all_actions(execution_context):
                return True
        return False

    def get_matching_triggers(self, triggers, execution_context):
        """get the first trigger which satisifies the condition"""
        return filter(lambda trigger: trigger.check_condition(execution_context), triggers)

    def wait_for_finish(self, execution_context):
        """Wait for the execution to finish"""
        execution_context.acquire_lock(timeout=self.timeout)
        if not execution_context.is_completed():
            raise TimeoutError()
        if execution_context.exception is not None:
            raise execution_context.exception # pylint: disable=E0702
        return execution_context.result

    def get_handlers(self, name):
        """get all handlers registered for an event"""
        if name in self.event_hook:
            return self.event_hook[name]
        return filter(lambda registered_name: self.match(name, registered_name), self.event_hook)

    def match(self, name, registered_name):
        """check if the name matched a registered name"""
        return re.match(registered_name, name)

    def stop_all_actions(self):
        """stop all executing actions"""
        if self.current_trigger is not None:
            stop_fn = getattr(self.current_trigger, 'stop', None)
            if callable(stop_fn):
                self.current_trigger.stop()
        time.sleep(0.1)
        for handler in self.stop_hooks:
            handler()

    def create_trigger(self, trigger_name):
        """Create a trigger from class name"""
        from . import class_loader
        trigger = class_loader.load_class(trigger_name)

        config = TriggerConfig()
        config.trigger = trigger
        return config

    def register_trigger(self, name, trigger):
        """Register a trigger and run it"""
        self.triggers.append(trigger)

        if name is None:
            return

        self.add_hook(name, trigger)

    def run_trigger(self, execution_context):
        """Run the trigger"""
        trigger = execution_context.trigger
        self.current_trigger = trigger

        try:
            execution_context.start_lock()
            return trigger.run(execution_context, self.app_context)
        except Exception as e:
            execution_context.reject(e)
            if self.error_handler is not None:
                self.error_handler.handle_error(e)
            else:
                logging.getLogger(__name__).error(e)
        finally:
            self.current_trigger = None

    def register_trigger_by_name(self, trigger_name,
                                 event=None,
                                 condition_str=None,
                                 stop_all_actions=None):
        """create and register the trigger"""
        trigger = self.create_trigger(trigger_name)
        if condition_str is not None and condition_str is not '':
            trigger.condition = TriggerCondition(condition_str)
        trigger.stop_all_actions = stop_all_actions
        self.register_trigger(event, trigger)
        return trigger
