"""Make the bot say"""

import json

from utils import http

class Pass(object):
    """Trigger to pass raw command to bot"""

    def run(self, execution_context, app_context):
        """run the action"""
        command = execution_context.event.get('command')
        url = app_context.get_config('bot.url')
        _, content = http.call(url, command)
        content_obj = json.loads(content.decode('utf-8'))
        execution_context.finish(content_obj['msg'])
