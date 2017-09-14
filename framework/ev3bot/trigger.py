"""Trigger framework"""

import re
import time
import logging
import threading
from enum import Enum
from queue import PriorityQueue, Empty

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
        self.priority = 0
        self.time_to_live = -1
        self.start_time = -1

    def start_lock(self):
        """start locking the context"""
        self.start_time = time.time()
        self.lock.acquire(blocking=False)

    def is_expired(self):
        """check if the execution is expired"""
        if self.time_to_live == -1:
            return False
        cur_time = time.time()
        return cur_time - self.start_time >= self.time_to_live

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

    def __cmp__(self, other):
        return (self.priority > other.priority) - (self.priority < other.priority)

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
        self.trigger = None
        self.priority = 0
        self.time_to_live = -1

    def set_extended_properties(self, extended_properties):
        """set the extended properties"""
        for prop_name in extended_properties:
            prop_value = extended_properties[prop_name]
            setattr(self, prop_name, prop_value)

    def check_condition(self, execution_context):
        """check if the condition is satisfied"""
        if self.condition is None:
            return True
        return self.condition.satisfied_by(execution_context)

class TriggerExecutionThread(threading.Thread):
    """Thread for watching and executing triggers"""

    def __init__(self, manager):
        threading.Thread.__init__(self)
        self.manager = manager
        self.stopped = False

    def run(self):
        while not self.stopped:
            try:
                execution_context = self.manager.queue.get_nowait()
                if execution_context.is_expired():
                    execution_context.reject(TimeoutError())
                else:
                    self.manager.run_trigger(execution_context)
            except Empty:
                time.sleep(0.001)

    def stop(self):
        """stop the thread"""
        self.stopped = True

class TriggerManager(object):
    """Manage all triggers"""

    def __init__(self):
        self.triggers = list()
        self.event_hook = dict()
        self.current_trigger = None
        self.current_trigger_priority = -1
        self.error_handler = None
        self.timeout = 3
        self.app_context = None
        self.stop_hooks = list()
        self.queue = PriorityQueue()
        self.executor = TriggerExecutionThread(self)
        self.executor.start()

    def on_shutdown(self):
        """function called on shutdown"""
        self.executor.stop()

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

        max_priority = max((config.priority for config in trigger_configs), default=-1)

        if max_priority > self.current_trigger_priority:
            self.stop_all_actions()

        result = None
        for config in trigger_configs:
            # build the execution context
            execution_context = TriggerExecutionContext(event, name, None)
            execution_context.trigger = config.trigger
            execution_context.trigger_manager = self
            execution_context.priority = config.priority
            execution_context.time_to_live = config.time_to_live
            execution_context.start_lock()

            if wait:
                self.queue.put(execution_context)
            else:
                result = self.run_trigger(execution_context)

        if not wait:
            return result

        return self.wait_for_finish(execution_context)

    def get_matching_triggers(self, trigger_configs, execution_context):
        """get the first trigger which satisifies the condition"""
        return list(filter(lambda cfg: cfg.check_condition(execution_context), trigger_configs))

    def wait_for_finish(self, execution_context):
        """Wait for the execution to finish"""
        execution_context.acquire_lock(timeout=self.timeout)
        if not execution_context.is_completed():
            return None
        if execution_context.exception is not None:
            raise execution_context.exception # pylint: disable=E0702
        return execution_context.result

    def get_handlers(self, name):
        """get all handlers registered for an event"""
        if name in self.event_hook:
            return self.event_hook[name]
        filtered = filter(lambda reg_name: self.match(name, reg_name), self.event_hook)
        name = next(filtered, None)
        return self.event_hook[name] if name is not None else list()

    def match(self, name, registered_name):
        """check if the name matched a registered name"""
        return re.match(registered_name, name)

    def stop_all_actions(self):
        """stop all executing actions"""
        if self.current_trigger is not None:
            stop_fn = getattr(self.current_trigger, 'stop', None)
            if callable(stop_fn):
                self.current_trigger.stop()
        for handler in self.stop_hooks:
            handler()

    def create_trigger(self, trigger_name):
        """Create a trigger from class name"""
        from . import class_loader
        trigger = class_loader.load_class(trigger_name)

        trigger_config = TriggerConfig()
        trigger_config.trigger = trigger
        return trigger_config

    def register_trigger(self, name, trigger_config):
        """Register a trigger and run it"""
        self.triggers.append(trigger_config)

        if name is None:
            return

        self.add_hook(name, trigger_config)

    def run_trigger(self, execution_context):
        """Run the trigger"""
        trigger = execution_context.trigger
        self.current_trigger = trigger
        self.current_trigger_priority = execution_context.priority

        try:
            return trigger.run(execution_context, self.app_context)
        except Exception as ex:
            execution_context.reject(ex)
            if self.error_handler is not None:
                self.error_handler.handle_error(ex)
            else:
                logging.getLogger(__name__).error(ex)
        finally:
            self.current_trigger = None
            self.current_trigger_priority = -1

    def register_trigger_by_name(self, trigger_name,
                                 event=None,
                                 condition_str=None,
                                 extended_properties=None):
        """create and register the trigger"""
        trigger_config = self.create_trigger(trigger_name)
        if condition_str is not None and condition_str is not '':
            trigger_config.condition = TriggerCondition(condition_str)
        if extended_properties is not None:
            trigger_config.set_extended_properties(extended_properties)
        self.register_trigger(event, trigger_config)
        return trigger_config
