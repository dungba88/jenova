"""Application bootstrap"""

import logging
from falcon import HTTPError

from orion.bootstrap import BaseBootstrap

from controllers import error
from controllers import IndexResource
from controllers import MessageResource

class ApplicationBootstrap(BaseBootstrap):
    """Bootstrap class"""

    def do_run(self):
        """Run the application"""
        self.register_error_handlers()
        self.register_routes()

    def register_error_handlers(self):
        """Register error handlers"""
        api = self.app_context.api
        api.add_error_handler(ValueError, error.value_error_handler)
        api.add_error_handler(HTTPError, error.http_error_handler)

        self.trigger_manager.error_handler = error.DefaultErrorHandler()

    def register_routes(self):
        """Register REST routes"""
        logging.info('Registering route')

        api = self.app_context.api
        api.add_route('/', IndexResource())
        api.add_route('/msg', MessageResource())

        logging.info('Route registered')
