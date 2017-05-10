"""Make the bot say"""

import json

from ev3bot.trigger import Trigger

from utils import http

class Pass(Trigger):
    """Trigger to pass raw command to bot"""

    def run(self, execution_context):
        command = execution_context.event.get('command')
        url = self.get_config('bot.url')
        _, content = http.call(url, command)
        content_obj = json.loads(content.decode('utf-8'))
        execution_context.finish(content_obj['msg'])
