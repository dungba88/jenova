"""Trigger implementation to sing"""

import random

from app import APP_INSTANCE as app
from utils import tts

def run(execution_context):
    """run the action"""
    song_id = execution_context.event.get('song_id', None)
    song = find_song(song_id)
    execution_context.finish('singing ' + song.get('name'))

    if song is not None:
        sing_the_song(song)

def find_song(song_id):
    """Find a song by id, or pick a random song if song_id is None"""
    songs = app.get_config('songs')

    if song_id is None:
        num_song = len(songs)
        rand_song_idx = random.randint(0, num_song - 1)
        return songs[rand_song_idx]
    else:
        return next(filter(lambda s: s.id == song_id, songs), None)

def sing_the_song(song):
    """Sing a specified song"""
    song_type = song.get('type')
    song_players = {
        'vocal': VocalSongPlayer()
    }
    song_players.get(song_type).play(song)

class VocalSongPlayer(object):
    """API for playing a song vocally"""
    def play(self, song):
        """Play a song by a TTS engine"""
        tts.say(song.get('lyrics'))
        