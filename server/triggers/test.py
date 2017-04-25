"""Trigger implementation for testing trained model"""

import logging

import nltk

from app import APP_INSTANCE as app
from utils import http
from utils.learn import pre_process
from utils.learn import persist
from utils.factory.tokenizer import TokenizerFactory

LOGGER = logging.getLogger(__name__)

def run(execution_context):
    """run the action"""
    filtered_word_type = app.get_config('predict.filtered_word_types')
    remove_stop_words = app.get_config('train.remove_stop_words')

    data_name = execution_context.event.get('data_name', 'default')
    text = execution_context.event.get('text')
    if text is None:
        raise ValueError('text cannot be null')

    config = persist.get_data_config(data_name)
    tokenizer = TokenizerFactory.get_tokenizer(config.get('tokenizer'))

    if config.get('clean_text'):
        text = pre_process.clean_text(text, remove_stop_words)

    tokenized_text = tokenizer(text)
    result_word, result_proba = pre_process.predict(tokenized_text, data_name)

    result_proba = result_proba * 100

    LOGGER.warning('predict %s with probability %2f %%', result_word, result_proba)

    pos_tagged_text = nltk.pos_tag(nltk.word_tokenize(text))
    filtered_text = \
        [(w, word_type) for w, word_type in pos_tagged_text if not word_type in filtered_word_type]

    result = 'predict: ' + result_word + ' with probability: ' \
                + str((int)(result_proba)) + '%'
    execution_context.finish(result)
    resp, content = send_msg(result_word, result_proba, filtered_text)
    # result = 'predict: ' + result_word + ' with probability: ' \
    #             + str((int)(result_proba)) + '%. response from bot: ' \
    #             + str(content)
    # execution_context.finish(result)

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
    return http.call(url, msg)
 