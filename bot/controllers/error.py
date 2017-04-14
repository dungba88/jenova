"""Error handling"""

from framework import encode

def value_error_handler(ex, req, resp, params):
    """Error handler for ValueError"""
    resp.body = encode.encode({
        'status': 1,
        'msg': 'Bad Request: ' + str(ex)
    })
