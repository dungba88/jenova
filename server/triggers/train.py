"""Trigger implementation for train"""

import csv
import json

from sklearn.externals import joblib

from app import APP_INSTANCE as app
from utils import pre_process
from utils.factory.vectorizer import VectorizerFactory
from utils.factory.algorithm import AlgorithmFactory

def run(execution_context):
    """run the action"""
    data_name = execution_context.event.get('name', 'default')
    with open('cache/data/' + data_name + '/raw.csv') as data_file:
        reader = csv.reader(data_file)
        train_data(reader, data_name)

def train_data(reader, data_name):
    """train the data file"""
    vectorizer = get_vectorizer()
    vectorized_data = pre_process.vectorize_data(reader, vectorizer)

    # save the data
    save_data(data_name, vectorized_data)

    # train the data
    algorithm = get_algorithm()
    model = algorithm.fit(vectorized_data.get('data'), vectorized_data.get('target'))

    # save the model
    save_model(data_name, model)

def get_vectorizer():
    """get the vectorizer based on config"""
    vectorizer_config = app.get_config('train.vectorizer')
    return VectorizerFactory.get_vectorizer(vectorizer_config)

def get_algorithm():
    """get the algorithm based on config"""
    algo_config = app.get_config('train.algorithm')
    return AlgorithmFactory.get_algorithm(algo_config)

def save_data(data_name, vectorized_data):
    """save the preprocessed data as file"""
    vector_file_data = {
        'data': vectorized_data.get('data'),
        'target': vectorized_data.get('target')
    }
    vocab_file_data = {
        'data_vocab': vectorized_data.get('data_vocab'),
        'target_vocab': vectorized_data.get('target_vocab')
    }
    with open('cache/data/' + data_name + '/vector.json', 'w') as vector_file:
        json.dump(vector_file_data, vector_file)

    with open('cache/data/' + data_name + '/vocab.json', 'w') as vocab_file:
        json.dump(vocab_file_data, vocab_file)

def save_model(data_name, model):
    """save the trained model to file"""
    joblib.dump(model, 'cache/data/' + data_name + '/model.pkl')
