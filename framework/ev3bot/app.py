"""Main application"""

from os import listdir
from os.path import join

import json
import falcon

from ev3bot.trigger import TriggerManager

class Application(object):
    """Main class, control application life-cycle and routing"""

    def __init__(self):
        self.api = falcon.API()
        self.trigger_manager = TriggerManager()
        self.configs = load_configs()
        self.bootstrap = None

    def run(self):
        """Run the application"""
        if self.bootstrap is not None:
            self.bootstrap.run()

    def get_config(self, name):
        """Get a config by name"""
        config_parts = name.split('.')
        obj = self.configs
        for part in config_parts:
            obj = obj.get(part, None)
            if obj is None:
                break
        return obj

def load_configs():
    """Load all configurations"""
    config = dict()
    for name in listdir('configs'):
        full_path = join('configs', name)
        name = name.replace('.json', '')
        with open(full_path) as data_file:
            config[name] = json.load(data_file)
    return config
