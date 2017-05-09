"""Make the bot say"""

from ev3bot.trigger import Trigger

from utils import http

class Say(Trigger):
    """Trigger to make the bot say a specific text"""

    def run(self, execution_context):
        text = execution_context.event.get('text')
        url = self.get_config('bot.url')
        msg = {
            'name': 'say',
            'args': {
                'text': text
            }
        }
        execution_context.finish(text)
        http.call(url, msg)
        