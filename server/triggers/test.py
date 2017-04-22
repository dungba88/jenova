"""Trigger implementation for testing trained model"""

import json
import logging

from httplib2 import Http
import nltk

from app import APP_INSTANCE as app
from utils.learn import pre_process

logger = logging.getLogger(__name__)

def run(execution_context):
    """run the action"""
    filtered_word_type = app.get_config('predict.filtered_word_types')
    remove_stop_words = app.get_config('train.remove_stop_words')

    data_name = execution_context.event.get('data_name', 'default')
    text = execution_context.event.get('text')
    if text is None:
        raise ValueError('text cannot be null')

    text = pre_process.clean_text(text, remove_stop_words)
    result_word, result_proba = pre_process.predict(text, data_name)

    logger.warning('predict %s with probability %2f %%', result_word, result_proba * 100)

    pos_tagged_text = nltk.pos_tag(nltk.word_tokenize(text))
    filtered_text = \
        [(w, word_type) for w, word_type in pos_tagged_text if not word_type in filtered_word_type]

#    send_msg(result_word, result_proba, filtered_text)

def send_msg(result_word, result_proba, filtered_text):
    """send the message to bot"""
    url = app.get_config('bot.url')
    msg = {
        'name': result_word,
        'args': {
            'proba': result_proba,
            'tagged_text': filtered_text
        }
    }
    http_client = Http()
    content = http_client.request(
        uri=url,
        method='POST',
        headers={'Content-Type': 'application/json; charset=UTF-8'},
        body=json.dumps(msg),
    )
    logger.info('response from bot: %s', content)
