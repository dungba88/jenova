"""Trigger framework"""

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

class TriggerManager(object):
    """Manage all triggers"""

    def __init__(self):
        self.triggers = list()
        self.event_hook = dict()

    def add_hook(self, name, handler):
        """Register a handler with an event name"""
        if name not in self.event_hook:
            self.event_hook[name] = list()
        self.event_hook[name].append(handler)

    def fire(self, name, event=None):
        """Fire the event, calling all handlers registered with the event"""
        if name not in self.event_hook:
            return
        for handler in self.event_hook[name]:
            handler(name, event)

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
        execution_context = TriggerExecutionContext(event, name, trigger)

        if trigger.condition is not None:
            if not trigger.condition.satisfied_by(execution_context):
                return

        trigger.action(execution_context)
