"""Trigger implementation for reload configuration"""

from utils import http

class Reload(object):
    """Trigger to reload the configuration"""
    def run(self, execution_context, _):
        """run the action"""
        from app import APP_INSTANCE as app
        app.reload_config()

        url = app.get_config('bot.url')
        msg = {
            'name': 'reload',
            'args': {}
        }
        execution_context.finish('reload done')
        http.call(url, msg)
