"""Trigger implementation for inquiring interest"""

from utils import tts

class InquireInterest(object):
    """Trigger to inquire the bot's interest"""

    def run(self, execution_context, app_context):
        """run the action"""
        interests = app_context.get_config('facts.tokenized_interests')
        has_interest_react = app_context.get_config('behavior.interest_react.yes')
        no_interest_react = app_context.get_config('behavior.interest_react.no')
        tagged_text = execution_context.event.get('tagged_text')

        for word in tagged_text:
            if word[1] == 'JJ' or word[1] == 'NN' or word[1] == 'NNS':
                if word[0] in interests:
                    tts.say_random_finish(has_interest_react, execution_context)
                    return

        tts.say_random_finish(no_interest_react, execution_context)
