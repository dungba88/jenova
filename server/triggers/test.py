"""Trigger implementation for testing trained model"""

import csv
import logging

from app import APP_INSTANCE as app
from utils.learn import classifier
from utils.learn import pre_process
from utils.learn import persist

LOGGER = logging.getLogger(__name__)

def run(execution_context):
    """run the action"""

    data_name = execution_context.event.get('data_name', 'default')

    config = persist.get_data_config(data_name)

    with open('cache/data/' + data_name + '/test.csv') as data_file:
        reader = csv.reader(data_file)
        result = test_data(reader, data_name, config)
        execution_context.finish(result)

def test_data(reader, data_name, config):
    """test the model"""
    remove_stop_words = app.get_config('train.remove_stop_words')

    input_texts, output_texts = pre_process.parse_csv(reader, config, remove_stop_words)
    target = pre_process.vectorize_target(output_texts, data_name)
    result = classifier.predict_list(input_texts, data_name)

    missed = (target != result).sum()

    result_proba = (1 - missed / len(target)) * 100

    return 'test against data name: ' + data_name + ' with accuracy: ' \
                + str((int)(result_proba)) + '%'
