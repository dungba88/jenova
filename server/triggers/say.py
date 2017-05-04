"""Make the bot say"""

from app import APP_INSTANCE as app
from utils import http

def run(execution_context):
    """run the action"""
    text = execution_context.event.get('text')
    url = app.get_config('bot.url')
    msg = {
        'name': 'say',
        'args': {
            'text': text
        }
    }
    execution_context.finish(text)
    http.call(url, msg)
    