"""Trigger implementation for train"""

import csv
import json

from app import APP_INSTANCE as app
from utils.learn import pre_process
from utils.learn import persist
from utils.factory.vectorizer import VectorizerFactory
from utils.factory.tokenizer import TokenizerFactory
from utils.factory.algorithm import AlgorithmFactory

def run(execution_context):
    """run the action"""
    data_name = execution_context.event.get('data_name', 'default')
    config = persist.get_data_config(data_name)

    with open('cache/data/' + data_name + '/raw.csv') as data_file:
        reader = csv.reader(data_file)
        train_data(reader, data_name, config)

    execution_context.finish('train done')

def train_data(reader, data_name, config):
    """train the data file"""
    remove_stop_words = app.get_config('train.remove_stop_words')
    input_texts, output_texts = pre_process.parse_csv(reader, config, remove_stop_words)

    vectorizer = get_vectorizer(config)
    vectorized_data = pre_process.vectorize_data(input_texts, output_texts, vectorizer)

    # save the data
    save_data(data_name, vectorized_data)

    # train the data
    algorithm = get_algorithm()
    model = algorithm.fit(vectorized_data.get('data'), vectorized_data.get('target'))

    # save the vectorizer
    persist.save_vectorizer(data_name, vectorizer)

    # save the model
    persist.save_model(data_name, model)

def get_vectorizer(config):
    """get the vectorizer based on config"""
    vectorizer_config = app.get_config('train.vectorizer')
    tokenizer_config = config.get('tokenizer')
    tokenizer = TokenizerFactory.get_tokenizer(tokenizer_config)
    return VectorizerFactory.get_vectorizer(vectorizer_config, tokenizer=tokenizer)

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
