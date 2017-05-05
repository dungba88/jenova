"""Trigger implementation for input"""

import csv

from app import APP_INSTANCE as app
from utils.learn import persist

def run(execution_context):
    """run the action"""
    event = execution_context.event
    data_name = event.get('data_name', 'default')
    text = event.get('text')

    validate(text)

    data_config = persist.get_data_config(data_name)
    if not data_config.get('allow_teaching'):
        raise ValueError('data_name ' + data_name + ' is not allowed to teach')

    with open("cache/data/" + data_name + '/raw.csv', 'a') as data_file:
        data_file.write(text)

    with open("cache/data/" + data_name + '/test.csv', 'a') as data_file:
        data_file.write(text)

def validate(text):
    """validate the input text"""
    if text is None or text is '':
        raise ValueError('text cannot be null')

    if not isinstance(text, str):
        raise ValueError('text must be string. ' + str(type(text))  + ' found.')

    max_input_length = app.get_config('train.max_input_length')
    if len(text) > max_input_length:
        raise ValueError('text length cannot be greater than ' + str(max_input_length))

    parts = list(csv.reader([text]))
    if len(parts[0]) != 2:
        raise ValueError('text must have exactly 2 comma-separated fragments')
