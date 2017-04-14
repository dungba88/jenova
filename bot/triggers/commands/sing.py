"""Trigger implementation to sing"""

import random

import app
from framework import tts

class SingTrigger(object):
    """Trigger class for singing a song"""

    def __init__(self):
        self.songs = app.get_config('songs')

    def init_trigger(self, manager):
        """create and register the trigger"""
        trigger = manager.create_trigger(self.sing_a_song)
        manager.register_trigger('sing', trigger)

    def sing_a_song(self, execution_context):
        """run the action"""
        song_id = execution_context.event.get('song_id', None)
        song = self.find_song(song_id)

        if song is not None:
            self.sing_the_song(song)

    def find_song(self, song_id):
        """Find a song by id, or pick a random song if song_id is None"""
        if song_id is None:
            num_song = len(self.songs)
            rand_song_idx = random.randint(0, num_song - 1)
            return self.songs[rand_song_idx]
        else:
            return next(filter(lambda s: s.id == song_id, self.songs), None)

    def sing_the_song(self, song):
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
        tts_engine_name = app.get_config('engine').get('tts_engine')
        tts.say(tts_engine_name, song.get('lyrics'))
