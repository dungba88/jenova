"""Trigger implementation for train"""

import csv
import json

from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib

from utils import pre_process

def run(execution_context):
    """run the action"""
    data_name = execution_context.event.get('name', 'default')
    with open('cache/data/' + data_name + '/raw.csv') as data_file:
        reader = csv.reader(data_file)
        train_data(reader, data_name)

def train_data(reader, data_name):
    """train the data file"""
    vectorized_data = pre_process.vectorize_data(reader)

    # save the data
    save_data(data_name, vectorized_data)

    # train the data
    gnb = GaussianNB()
    model = gnb.fit(vectorized_data.get('data'), vectorized_data.get('target'))

    # save the model
    save_model(data_name, model)

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
