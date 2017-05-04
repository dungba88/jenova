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
    filtered_word_types = app.get_config('train.filtered_word_types')

    input_texts, output_texts = pre_process.parse_csv(reader, config, filtered_word_types)
    target, target_vocab = pre_process.vectorize_target(output_texts, data_name)
    result = classifier.predict_list(input_texts, data_name)

    missed = target != result
    missed_count = missed.sum()
    idxes = [idx for idx, value in enumerate(missed) if value]
    missed_sentences = [build_sentence(idx, input_texts, target_vocab, result) for idx in idxes]

    result_proba = (1 - missed_count / len(target)) * 100

    return 'test against data name: ' + data_name + ' with accuracy: ' \
                + str((int)(result_proba)) + '%. Missed: ' \
                + '. '.join(missed_sentences)

def build_sentence(idx, input_texts, target_vocab, result):
    """build a sentence"""
    return input_texts[idx] + "(" + str(target_vocab[result[idx]]) + ")"
