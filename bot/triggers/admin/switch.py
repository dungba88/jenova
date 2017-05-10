"""Trigger implementation for reload configuration"""

import re

from ev3bot.trigger import Trigger

class Switch(Trigger):
    """Trigger to switch the bot"""

    def run(self, execution_context):
        pattern = r'^[\w_]+$'
        bot_name = execution_context.event.get('bot')
        if bot_name is None or bot_name is '':
            raise ValueError('bot name cannot be null or empty')
        if not re.match(pattern, bot_name):
            raise ValueError('bot name can only contains alphanumeric characters and underscore')
        from app import APP_INSTANCE as app
        app.reload_config(bot_name)
        execution_context.finish('switched to ' + bot_name)
