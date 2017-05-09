"""twitter api"""

import json
import ssl
from pathlib import Path

def create_api():
    """create a twitter api"""
    from twitter import OAuth, Twitter

    from app import APP_INSTANCE as app
    access_token = app.get_config('api.twitter.access_token')
    access_secret = app.get_config('api.twitter.access_secret')
    consumer_key = app.get_config('api.twitter.consumer_key')
    consumer_secret = app.get_config('api.twitter.consumer_secret')

    # temporary fix for certificate error
    ssl._create_default_https_context = ssl._create_unverified_context

    oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)

    # Initiate the connection to Twitter API
    return Twitter(auth=oauth)

def get_statuses(tweet_count=20):
    """get all twitter statuses"""
    cached = get_cache('statuses')
    if cached is not None:
        return cached

    twitter = create_api()

    tweets = twitter.statuses.home_timeline(count=tweet_count)

    save_cache('statuses', tweets)

    return tweets

def iterator_to_list(iterator, size):
    """convert iterator to list with size"""
    result = []
    for item in iterator:
        size -= 1
        result.append(item)
        if size <= 0:
            break
    return result

def save_cache(cache_type, obj):
    """save the cache"""
    cache_file_name = get_cache_file(cache_type)
    with open(cache_file_name, 'w+') as cache_data_file:
        json.dump(obj, cache_data_file)

def get_cache(cache_type):
    """get cached data by type"""
    cache_file_name = get_cache_file(cache_type)
    cache_file = Path(cache_file_name)
    file_exists = cache_file.is_file()

    if not file_exists:
        return None

    with open(cache_file_name) as cache_data_file:
        return json.load(cache_data_file)

def get_cache_file(cache_type):
    """Get cache file for a specific type"""
    return "cache/twitter/" + cache_type + ".json"
