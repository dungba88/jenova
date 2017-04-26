"""Trigger implementation for reload configuration"""

from app import APP_INSTANCE as app
from utils import http

def run(execution_context):
    """run the action"""
    app.reload_config()

    url = app.get_config('bot.url')
    msg = {
        'name': 'reload',
        'args': {
        }
    }
    execution_context.finish()
    http.call(url, msg)
