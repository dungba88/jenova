"""Message view"""

from orion import encode

class MessageResource(object):
    """Controller for message resource"""

    def __init__(self, trigger_manager):
        self.trigger_manager = trigger_manager

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
            execution_context = self.trigger_manager.fire(msg_name, msg_args)
            if execution_context is not None:
                execution_result = execution_context.wait_for_finish(timeout=3000)
            else:
                execution_result = None
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
