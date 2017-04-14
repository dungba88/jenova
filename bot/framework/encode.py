"""Utility for encode/decode object"""

import json

def encode(result):
    """encode the result by JSON"""
    return json.dumps(result)

def decode(body):
    """decode string to object"""
    if not body:
        return None
    return json.loads(body)

def decode_from_request(req):
    """decode the request body to object"""
    req_body = req.stream.read()
    return decode(req_body.decode('utf-8'))
    