"""Error handling"""

from ev3bot import encode
import traceback

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
