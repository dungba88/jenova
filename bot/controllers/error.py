"""Error handling"""

from ev3bot import encode
from falcon import HTTPError

from utils import tts
import traceback

def distress_call(ex):
    tts.say(["Alert! " + str(ex) + ". Please check urgently!"])

def default_error_handler(ex, req, resp, params):
    """Error handler for all exceptions"""
    error_handlers = {
        ValueError: value_error_handler,
        HTTPError: http_error_handler,
        BaseException: base_error_handler
    }
    for ex_type in error_handlers:
        if isinstance(ex, ex_type):
            handler = error_handlers.get(ex_type)
            handler(ex, req, resp, params)
            break

    distress_call(ex)

def value_error_handler(ex, req, resp, params):
    """Error handler for ValueError"""
    resp.body = encode.encode({
        'status': 1,
        'msg': 'Bad Request: ' + str(ex)
    })

def base_error_handler(ex, req, resp, params):
    """Error handler for BaseException"""
    resp.body = encode.encode({
        'status': 1,
        'msg': 'Uncaught exception: ' + str(ex),
        'exception': traceback.format_exception(None, # <- type(e) by docs, but ignored
                                                ex, ex.__traceback__)
    })

def http_error_handler(ex, req, resp, params):
    """Error handler for HTTPError"""
    resp.body = encode.encode({
        'status': 1,
        'msg': 'HTTP error: ' + ex.status
    })
