"""Main application"""

from os import listdir
from os.path import join

import logging
import json
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
        self.configs = self.load_configs()
        print(self.configs)

    def load_configs(self):
        """Load all configurations"""
        config = dict()
        for name in listdir('configs'):
            full_path = join('configs', name)
            name = name.replace('.json', '')
            with open(full_path) as f:
                config[name] = json.load(f)
        return config

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

def get_config(name):
    """Get a config by name"""
    config_parts = name.split('.')
    obj = APP_INSTANCE.configs
    for part in config_parts:
        obj = obj.get(part, None)
        if obj is None:
            break
    return obj
