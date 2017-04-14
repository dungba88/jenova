"""Main application"""

import logging
import falcon
from falcon import HTTPError

from framework.trigger import TriggerManager
from controllers import IndexResource
from controllers import MessageResource
from controllers import error
import triggers

class Application(object):
    """Main class, control application life-cycle and routing"""

    def __init__(self):
        self.api = falcon.API()
        self.trigger_manager = TriggerManager()

    def run(self):
        """Run the application"""
        self.register_error_handlers()
        self.register_routes()
        self.register_triggers()

    def register_error_handlers(self):
        """Register error handlers"""
        self.api.add_error_handler(ValueError, error.value_error_handler)
        self.api.add_error_handler(HTTPError, error.http_error_handler)

    def register_routes(self):
        """Register REST routes"""
        logging.info('Registering route')

        self.api.add_error_handler(ValueError, error.value_error_handler)

        self.api.add_route('/', IndexResource())
        self.api.add_route('/msg', MessageResource())

        logging.info('Route registered')

    def register_triggers(self):
        """Register triggers"""
        logging.info('Registering triggers')

        triggers.init_all_triggers(self.trigger_manager)

        logging.info('Trigger registered')

# singleton instance
APP_INSTANCE = Application()
