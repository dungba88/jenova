"""Application bootstrap"""

import logging

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
        self.register_locale()

    def register_locale(self):
        """register locale based on config"""
        import locale
        locale.setlocale(locale.LC_ALL, self.app_context.get_config('facts.locale'))

    def register_error_handlers(self):
        """Register error handlers"""
        api = self.app_context.api
        api.add_error_handler(BaseException, error.default_error_handler)

        self.trigger_manager.error_handler = error.BotErrorHandler()

    def register_routes(self):
        """Register REST routes"""
        logging.info('Registering route')

        api = self.app_context.api
        api.add_route('/', IndexResource())
        api.add_route('/msg', MessageResource())

        logging.info('Route registered')
