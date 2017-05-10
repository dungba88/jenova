"""Trigger implementation to tell a story"""

import time
import random

from ev3bot.trigger import Trigger

from utils import tts

class Story(Trigger):
    """Trigger to tell a story"""

    def __init__(self):
        Trigger.__init__(self)
        self.stopped = False

    def run(self, execution_context):
        """run the action"""
        self.stopped = False
        openings = self.get_config('story.opening')
        no_story = self.get_config('story.no_story')
        pause_time = self.get_config('story.pause_time')
        stories = self.get_config('story.stories')
        tag = execution_context.event.get('tag', None)

        if tag is not None:
            # filter stories based on tags
            stories = list(filter(lambda story: tag in story.get('tags'), stories))

        if len(stories) == 0:
            execution_context.finish('no story')
            tts.say_random(no_story)
            return

        story = stories[random.randint(0, len(stories) - 1)]
        execution_context.finish('telling ' + story.get('name'))

        tts.say_random(openings)

        time.sleep(pause_time)

        if self.stopped:
            return

        with open('cache/stories/' + story.get('file')) as data_file:
            text = data_file.read()
            self.read_long_text(text)

    def read_long_text(self, text):
        """Read a possibly long text"""
        for line in text.splitlines():
            if not self.stopped and len(line) > 0:
                tts.say([line])

    def stop(self):
        """stop reading the story"""
        self.stopped = True
