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

def load_vectorizer(data_name):
    """load vocab from file"""
    return joblib.load('cache/data/' + data_name + '/vectorizer.pkl')

def get_data_config(data_name):
    """get data config"""
    with open('cache/data/' + data_name + '/config.json') as config_file:
        return json.load(config_file)

def save_model(data_name, model):
    """save the trained model to file"""
    joblib.dump(model, 'cache/data/' + data_name + '/model.pkl')

def save_vectorizer(data_name, vectorizer):
    """save the trained model to file"""
    joblib.dump(vectorizer, 'cache/data/' + data_name + '/vectorizer.pkl')
