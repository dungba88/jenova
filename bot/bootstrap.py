"""Application bootstrap"""

import logging
from falcon import HTTPError

from controllers import error
from controllers import IndexResource
from controllers import MessageResource
import triggers

class ApplicationBootstrap(object):
    """Bootstrap class"""

    def __init__(self):
        self.app = None

    def run(self):
        """Run the application"""
        self.register_error_handlers()
        self.register_routes()
        self.register_triggers()

    def register_error_handlers(self):
        """Register error handlers"""
        api = self.app.api
        api.add_error_handler(ValueError, error.value_error_handler)
        api.add_error_handler(HTTPError, error.http_error_handler)

    def register_routes(self):
        """Register REST routes"""
        logging.info('Registering route')

        api = self.app.api
        api.add_route('/', IndexResource())
        api.add_route('/msg', MessageResource())

        logging.info('Route registered')

    def register_triggers(self):
        """Register triggers"""
        logging.info('Registering triggers')

        triggers.init_all_triggers(self.app.trigger_manager)

        logging.info('Trigger registered')
