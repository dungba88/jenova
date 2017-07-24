"""Application bootstrap"""

import logging
from falcon import HTTPError

from controllers import error
from controllers import IndexResource
from controllers import MessageResource

class ApplicationBootstrap(object):
    """Bootstrap class"""

    def __init__(self):
        self.app_context = None
        self.trigger_manager = None

    def run(self):
        """Run the application"""
        self.register_error_handlers()
        self.register_routes()
        self.init_caffe()

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

    def init_caffe(self):
        """initialize caffe models"""
