"""Trigger implementation to sing"""

import json
import random

from ev3bot.trigger import Trigger

from utils import tts

NOTE_FREQ = {
    "C4": 261.6,
    "C#4": 277.2,
    "D4": 293.7,
    "D#4": 311.1,
    "E4": 329.6,
    "F4": 349.2,
    "F#4": 370.0,
    "G4": 392.0,
    "G#4": 415.3,
    "A4": 440.0,
    "A#4": 466.2,
    "B4": 493.9,
    "C5": 523.3,
    "C#5": 554.4,
    "D5": 587.3,
    "D#5": 622.3,
    "E5": 659.3,
    "F5": 698.5,
    "F#5": 740.0,
    "G5": 784.0,
    "G#5": 415.3,
    "A5": 830.6,
    "A#5": 880.0,
    "B5": 987.8
}

class Sing(Trigger):
    """Trigger to sing a song"""
    def run(self, execution_context):
        song_id = execution_context.event.get('song_id', None)
        song = self.find_song(song_id)
        execution_context.finish('singing ' + song.get('name'))

        if song is not None:
            self.sing_the_song(song)

    def find_song(self, song_id):
        """Find a song by id, or pick a random song if song_id is None"""
        songs = self.get_config('songs')

        if song_id is None:
            num_song = len(songs)
            rand_song_idx = random.randint(0, num_song - 1)
            return songs[rand_song_idx]
        else:
            return next(filter(lambda s: s['id'] == song_id, songs), None)

    def sing_the_song(self, song):
        """Sing a specified song"""
        song_type = song.get('type')
        song_players = {
            'vocal': VocalSongPlayer(),
            'tone': ToneSongPlayer(),
            'wav': WavSongPlayer(),
            'beep': BeepSongPlayer()
        }
        song_players.get(song_type).play(song)

class VocalSongPlayer(object):
    """API for playing a song vocally"""
    def play(self, song):
        """Play a song by a TTS engine"""
        tts.say(song.get('lyrics'))

class ToneSongPlayer(object):
    """API for playing a song with tones"""
    def play(self, song):
        """Play the song"""
        from ev3dev.ev3 import Sound
        file_name = song.get('file_name')
        with open(file_name) as data_file:
            lyrics = json.load(data_file)
            Sound.tone(self.convert_lyrics(lyrics)).wait()

    def convert_lyrics(self, lyrics):
        """convert lyrics to EV3 format"""
        result = list()
        for lyric in lyrics:
            result.append((NOTE_FREQ[lyric[0]], lyric[1], lyric[2]))
        return result

class WavSongPlayer(object):
    """API for playing a WAV file"""
    def play(self, song):
        """Play the song"""
        file_name = song.get('file_name')
        from ev3dev.ev3 import Sound
        Sound.play(file_name).wait()

class BeepSongPlayer(object):
    """API for playing a song with beeps"""
    def play(self, song):
        """Play the song"""
        file_name = song.get('file_name')
        with open(file_name) as data_file:
            lyrics = data_file.read()
            from ev3dev.ev3 import Sound
            Sound.beep(lyrics).wait()
