"""persistent module"""

import json

from sklearn.externals import joblib

def load_vocab_file(data_name):
    """load vocab from file"""
    with open('cache/data/' + data_name + '/vocab.json') as vocab_file:
        return json.load(vocab_file)

def load_model_file(data_name):
    """load vocab from file"""
    return joblib.load('cache/data/' + data_name + '/model.pkl')
