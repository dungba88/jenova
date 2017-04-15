"""MaryTTS engine"""

import hashlib
from pathlib import Path
from urllib.parse import urlencode

from httplib2 import Http
from ev3bot import audio

class MaryTTS(object):
    """Wrapper class for MaryTTS"""
    def __init__(self, config):
        self.config = config

    def say(self, texts):
        """Speak the texts"""
        for text in texts:
            self.speak_text(text)

    def speak_text(self, text):
        """Speak a single text"""
        if not self.cache_file_exist(text):
            self.download(text)
        self.play(text)

    def cache_file_exist(self, text):
        """Check if cache file exists for a specific text"""
        cache_file_name = self.get_cache_file(text)
        cache_file = Path(cache_file_name)
        return cache_file.is_file()

    def download(self, text):
        """Download a text from server"""
        query = self.build_query(text)
        http_client = Http()
        url = "http://%s:%s/process?" % (self.config.host, self.config.port)
        resp, content = http_client.request(url, "POST", query)
        if resp["content-type"] == "audio/x-wav":
            self.save(text, content)
        else:
            raise Exception(content)

    def save(self, text, content):
        """Save a WAV file"""
        file_name = self.get_cache_file(text)
        wave_file = open(file_name, "wb")
        wave_file.write(content)
        wave_file.close()

    def play(self, text):
        """Play a saved text"""
        file_name = self.get_cache_file(text)
        audio.play(file_name)

    def get_cache_file(self, text):
        """Get cache file for a specific text"""
        text_hash = hashlib.md5(text).hexdigest()
        return "cache/sound/mary_" + text_hash + ".WAV"

    def build_query(self, text):
        """build a query to MaryTTS server"""
        query_hash = {
            "INPUT_TEXT": text,
            "INPUT_TYPE": "TEXT", # Input text
            "LOCALE": self.config.locale,
            "VOICE": self.config.voice, # Voice informations  (need to be compatible)
            "OUTPUT_TYPE": "AUDIO",
            "AUDIO":"WAVE", # Audio informations (need both)
        }

        return urlencode(query_hash)
