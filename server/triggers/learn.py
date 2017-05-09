"""Trigger implementation for input"""

from ev3bot.trigger import Trigger

class Learn(Trigger):
    """Trigger to learn new sample"""

    def run(self, execution_context):
        event = execution_context.event
        data_file = event.get('data_file', 'default')
        input_text = event.get('input')
        output_type = event.get('output_type')
        output_args = event.get('output_args')

        self.validate(input_text, output_type, output_args)

        # insert the document
        document = {
            'input': input_text,
            'output_type': output_type,
            'output_args': output_args
        }
        #TODO save to file

    def validate(self, input_text, output_type, output_args):
        """validate input and output"""
        if input_text is None or output_type is None:
            raise ValueError('input and output_type parameters cannot be null')

        if output_args is not None and not isinstance(output_args, dict):
            raise ValueError('output_args must be instance of dict')
