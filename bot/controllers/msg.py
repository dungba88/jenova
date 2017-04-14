"""Message view"""

from framework import encode
from app import APP_INSTANCE as app

class MessageResource(object):
    """Controller for message resource"""

    def on_post(self, req, res):
        """Handle POST method"""

        msg = encode.decode_from_request(req)
        if msg is None:
            raise ValueError('msg cannot be empty')

        msg_name = msg.get('name')
        msg_args = msg.get('args', dict())

        app.trigger_manager.fire(msg_name, msg_args)

        result = {
            'status': 0,
            'message': msg_name
        }
        res.body = encode.encode(result)
        