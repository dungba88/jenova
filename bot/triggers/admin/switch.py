"""Trigger implementation for reload configuration"""

from ev3bot.trigger import Trigger

class Switch(Trigger):
    """Trigger to switch the bot"""

    def run(self, execution_context):
        bot_name = execution_context.event.get('bot')
        from app import APP_INSTANCE as app
        app.reload_config(bot_name)
        execution_context.finish('switched to ' + bot_name)
