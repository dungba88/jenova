"""Trigger implementation for testing trained model"""

import csv

from utils.learn import classifier
from utils.learn import pre_process
from utils.learn import persist

class Test(object):
    """Trigger to test the accuracy of the trained model"""
    def run(self, execution_context, app_context):
        """run the action"""
        data_name = execution_context.event.get('data_name', 'default')

        config = persist.get_data_config(data_name)

        filtered_word_types = app_context.get_config('train.filtered_word_types')

        with open('cache/data/' + data_name + '/test.csv') as data_file:
            reader = csv.reader(data_file)
            result = self.test_data(reader, data_name, config, filtered_word_types)
            execution_context.finish(result)

    def test_data(self, reader, data_name, config, filtered_word_types):
        """test the model"""

        # parse the csv
        input_texts, output_texts = pre_process.parse_csv(reader, config, filtered_word_types)

        # vectorize outputs
        target, target_vocab = pre_process.vectorize_target(output_texts, data_name)

        # predict the test set
        result = classifier.predict_list(input_texts, data_name)

        # find the misclassified samples
        missed = target != result

        missed_count = missed.sum()

        # get the indexes of the misclassified samples
        idxes = [idx for idx, value in enumerate(missed) if value]

        # map the indexes to corresponding sentences in test set
        missed_sentences = [self.build_sentence(idx, input_texts, target_vocab, result) \
                             for idx in idxes]

        accuracy = (1 - missed_count / len(target)) * 100

        return 'test against data name: ' + data_name + ' with accuracy: ' \
                    + str((int)(accuracy)) + '%. Missed: ' \
                    + '. '.join(missed_sentences)

    def build_sentence(self, idx, input_texts, target_vocab, result):
        """build a sentence"""
        return input_texts[idx] + "(" + str(target_vocab[result[idx]]) + ")"
