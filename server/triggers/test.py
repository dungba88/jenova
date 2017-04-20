"""Trigger implementation for testing trained model"""

import json

from sklearn.externals import joblib

from app import APP_INSTANCE as app
from utils import pre_process

def run(execution_context):
    """run the action"""
    remove_stop_words = app.get_config('train.remove_stop_words')
    data_name = execution_context.event.get('data_name', 'default')
    text = execution_context.event.get('text')
    if text is None:
        raise ValueError('text cannot be null')

    vocab = load_vocab_file(data_name)
    model = load_model_file(data_name)


    text = pre_process.clean_text(text, remove_stop_words)
    vectorized_text = pre_process.vectorize_new_input(text, vocab.get('data_vocab'))
    ypred = model.predict([vectorized_text])
    print(vocab.get('target_vocab')[ypred[0]])

def load_vocab_file(data_name):
    """load vocab from file"""
    with open('cache/data/' + data_name + '/vocab.json') as vocab_file:
        return json.load(vocab_file)

def load_model_file(data_name):
    """load vocab from file"""
    return joblib.load('cache/data/' + data_name + '/model.pkl')
