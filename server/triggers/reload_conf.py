"""Trigger implementation for reload configuration"""

from ev3bot.trigger import Trigger

from utils import http

class Reload(Trigger):
    """Trigger to reload the configuration"""
    def run(self, execution_context):
        from app import APP_INSTANCE as app
        app.reload_config()

        url = app.get_config('bot.url')
        msg = {
            'name': 'reload',
            'args': {}
        }
        execution_context.finish('reload done')
        http.call(url, msg)
