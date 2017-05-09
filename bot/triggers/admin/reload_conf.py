"""Trigger implementation for reload configuration"""

from ev3bot.trigger import Trigger

class Reload(Trigger):
    """Trigger to reload the config"""

    def run(self, execution_context):
        from app import APP_INSTANCE as app
        app.reload_config()
        execution_context.finish()
