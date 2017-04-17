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

    if len(stories) == 0:
        tts.say_random(no_story)
        return

    story = stories[random.randint(0, len(stories) - 1)]

    tts.say_random(openings)
    time.sleep(pause_time)
    if FLAGS["stop"]:
        return
    with open('cache/stories/' + story) as data_file:
        text = data_file.read()
        for line in text.splitlines():
            if not FLAGS["stop"]:
                if len(line) > 0:
                    tts.say([line])

def stop_story():
    """stop reading the story"""
    FLAGS["stop"] = True
