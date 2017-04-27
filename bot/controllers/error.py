"""Error handling"""

from ev3bot import encode
from falcon import HTTPError
import logging

from utils import tts
import traceback

logger = logging.getLogger(__name__)

class BotErrorHandler(object):
    """error handler for bot"""

    def handle_error(self, ex):
        """handle error"""
        default_error_handler(ex, None, None, None)

def distress_call(ex):
    """Broadcast a distress call"""
    tts.say(["Alert! " + str(ex) + ". Please check urgently!"])
    traces = traceback.format_exception(None, # <- type(e) by docs, but ignored
                                        ex, ex.__traceback__)
    for trace in traces:
        logger.error(trace)

def default_error_handler(ex, req, resp, params):
    """Error handler for all exceptions"""
    error_handlers = {
        ValueError: value_error_handler,
        HTTPError: http_error_handler,
        BaseException: base_error_handler
    }
    if resp is not None:
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
    if resp is None:
        return
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
