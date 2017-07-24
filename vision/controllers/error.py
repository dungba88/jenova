"""Error handling"""

import logging
import traceback

from ev3bot import encode

class DefaultErrorHandler(object):
    """default error handler class"""

    def handle_error(self, ex):
        """handle error"""
        default_error_handler(ex)

def default_error_handler(ex):
    """Error handler for all exceptions"""
    logger = logging.getLogger(__name__)
    traces = traceback.format_exception(None, # <- type(e) by docs, but ignored
                                        ex, ex.__traceback__)
    for trace in traces:
        logger.error(trace)

def value_error_handler(ex, req, resp, params):
    """Error handler for ValueError"""
    resp.body = encode.encode({
        'status': 1,
        'msg': 'Bad Request: ' + str(ex)
    })

def http_error_handler(ex, req, resp, params):
    """Error handler for HTTPError"""
    resp.body = encode.encode({
        'status': 1,
        'msg': 'HTTP error: ' + ex.status
    })
