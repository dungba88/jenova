"""Trigger implementation to tell a story"""

import time
import random

from app import APP_INSTANCE as app
from utils import tts

FLAGS = {
    "stop": False
}

def run(execution_context):
    """run the action"""
    FLAGS["stop"] = False
    openings = app.get_config('behavior.story.opening')
    no_story = app.get_config('behavior.story.no_story')
    pause_time = app.get_config('behavior.story.pause_time')
    stories = app.get_config('behavior.story.stories')
    tag = execution_context.event.get('tag', None)

    if tag is not None:
        # filter stories based on tags
        stories = list(filter(lambda story: tag in story.get('tags'), stories))

    if len(stories) == 0:
        tts.say_random(no_story)
        return

    tts.say_random(openings)

    time.sleep(pause_time)

    if FLAGS["stop"]:
        return

    story = stories[random.randint(0, len(stories) - 1)]
    with open('cache/stories/' + story.get('file')) as data_file:
        text = data_file.read()
        read_long_text(text)

def read_long_text(text):
    """Read a possibly long text"""
    for line in text.splitlines():
        if not FLAGS["stop"] and len(line) > 0:
            tts.say([line])

def stop_story():
    """stop reading the story"""
    FLAGS["stop"] = True
