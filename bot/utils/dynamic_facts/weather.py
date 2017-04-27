"""weather facts"""

import json
import time
import logging

from app import APP_INSTANCE as app
from utils import http

LOGGER = logging.getLogger(__name__)

CACHED_DATA = {
    'CACHED_RESULT': None,
    'CACHED_TIME': 0
}

def get_weather(city=None):
    """get weather forecast"""
    global CACHED_DATA
    time_to_live = app.get_config('api.weather.time_to_live')
    if has_cache(time_to_live):
        LOGGER.warning('Use cached weather data')
        return CACHED_DATA['CACHED_RESULT']
    app_id = app.get_config('api.weather.key')
    # TODO get city dynamically
    if city is None:
        city = app.get_config('api.weather.city')
    server_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&APPID=' + app_id
    res, content = http.call(server_url, None, 'GET')
    result = json.loads(content.decode('utf-8'))
    if result is None or result.get('cod') != 200:
        LOGGER.warning('Result from api server: ' + str(content))
        return None
    CACHED_DATA['CACHED_RESULT'] = result
    CACHED_DATA['CACHED_TIME'] = time.time()
    return result

def has_cache(time_to_live):
    """check if the weather cache is available"""
    cached_time = time.time() - CACHED_DATA['CACHED_TIME']
    return CACHED_DATA['CACHED_RESULT'] is not None and cached_time < time_to_live
