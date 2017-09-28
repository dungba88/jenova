"""Trigger implementation for reload configuration"""

class Reload(object):
    """Trigger to reload the config"""

    def run(self, execution_context, _):
        """run the action"""
        from app import APP_INSTANCE as app
        app.reload_config()
        execution_context.finish()
