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
        self.app_context = ApplicationContext(trigger_manager=self.trigger_manager,
                                              api=self.api,
                                              configs=self.configs)

    def run(self):
        """Run the application"""
        if self.bootstrap is not None:
            self.bootstrap.app_context = self.app_context
            self.bootstrap.run()

    def get_config(self, name):
        """Get a config by name"""
        if self.app_context is not None:
            return self.app_context.get_config(name)
        return None

class ApplicationContext(object):
    """Application context"""
    def __init__(self, trigger_manager, api, configs):
        self.trigger_manager = trigger_manager
        self.api = api
        self.configs = configs
        self.params = dict()

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
    files = filter(lambda file: ".json" in file, listdir('configs'))
    for name in files:
        full_path = join('configs', name)
        name = name.replace('.json', '')
        with open(full_path) as data_file:
            config[name] = json.load(data_file)
    return config
