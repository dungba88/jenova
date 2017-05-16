"""Application bootstrap"""

import logging

from controllers import error
from controllers import IndexResource
from controllers import MessageResource

from utils.ev3.sensor_readings import SensorReadings

class ApplicationBootstrap(object):
    """Bootstrap class"""

    def __init__(self):
        self.app_context = None
        self.trigger_manager = None
        self.sensor_readings = None

    def run(self):
        """Run the application"""
        self.trigger_manager.fire('app_starting')
        self.register_error_handlers()
        self.register_routes()
        self.register_locale()
        self.register_sensors()
        self.trigger_manager.fire('app_started')

    def register_sensors(self):
        """register sensors readings"""
        self.sensor_readings = SensorReadings(self.trigger_manager, self.app_context)
        self.sensor_readings.run()

    def register_locale(self):
        """register locale based on config"""
        import locale
        locale.setlocale(locale.LC_ALL, self.app_context.get_config('facts.locale'))

    def register_error_handlers(self):
        """Register error handlers"""
        api = self.app_context.api
        api.add_error_handler(BaseException, error.default_error_handler)

        self.trigger_manager.error_handler = error.BotErrorHandler()

        from ev3bot import audio
        self.trigger_manager.add_stop_hook(audio.stop)

    def register_routes(self):
        """Register REST routes"""
        logging.info('Registering route')

        api = self.app_context.api
        api.add_route('/', IndexResource())
        api.add_route('/msg', MessageResource())

        logging.info('Route registered')
