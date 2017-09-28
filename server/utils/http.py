"""http utils"""

import logging
import json

from httplib2 import Http

LOGGER = logging.getLogger(__name__)

def call(url, msg):
    """call http service"""
    http_client = Http()
    resp, content = http_client.request(
        uri=url,
        method='POST',
        headers={'Content-Type': 'application/json; charset=UTF-8'},
        body=json.dumps(msg),
    )
    LOGGER.info('response from bot: %s', resp)
    LOGGER.info('response from bot: %s', content)
    return resp, content
