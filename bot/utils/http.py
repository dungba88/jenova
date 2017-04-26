"""http utils"""

import logging
import json

from httplib2 import Http

LOGGER = logging.getLogger(__name__)

def call(url, msg, method='POST'):
    """call http service"""
    body = None
    if msg is not None:
        body = json.dumps(msg)

    http_client = Http()
    resp, content = http_client.request(
        uri=url,
        method=method,
        headers={'Content-Type': 'application/json; charset=UTF-8'},
        body=body,
    )
    return resp, content
