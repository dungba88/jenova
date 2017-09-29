"""Message view"""

from orion import encode
from app import APP_INSTANCE as app

class MessageResource(object):
    """Controller for message resource"""

    def on_post(self, req, res):
        """Handle POST method"""
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin")
        res.set_header('Access-Control-Allow-Headers', \
                       'Origin, X-Requested-With, Content-Type, Accept')

        msg = encode.decode_from_request(req)
        if msg is None:
            raise ValueError('msg cannot be empty')

        msg_name = msg.get('name')
        msg_args = msg.get('args', dict())

        try:
            execution_context = app.trigger_manager.fire(msg_name, msg_args)
            execution_result = execution_context.wait_for_finish(timeout=3000)
            result = {
                'status': 0,
                'msg': execution_result
            }
        except Exception as ex:
            result = {
                'status': 1,
                'msg': type(ex).__name__ + ': ' + str(ex)
            }

        res.body = encode.encode(result)
