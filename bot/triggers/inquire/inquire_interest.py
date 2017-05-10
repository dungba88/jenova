"""Trigger implementation for inquiring interest"""

from ev3bot.trigger import Trigger

from utils import tts

class InquireInterest(Trigger):
    """Trigger to inquire the bot's interest"""

    def run(self, execution_context):
        interests = self.get_config('facts.tokenized_interests')
        has_interest_react = self.get_config('behavior.interest_react.yes')
        no_interest_react = self.get_config('behavior.interest_react.no')
        tagged_text = execution_context.event.get('tagged_text')

        for word in tagged_text:
            if word[1] == 'JJ' or word[1] == 'NN' or word[1] == 'NNS':
                if word[0] in interests:
                    tts.say_random_finish(has_interest_react, execution_context)
                    return

        tts.say_random_finish(no_interest_react, execution_context)
