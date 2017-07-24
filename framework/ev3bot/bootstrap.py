"""Application bootstrap"""

class BaseBootstrap(object):
    """Bootstrap class"""

    def __init__(self):
        self.app_context = None
        self.trigger_manager = None

    def run(self):
        """Run the application"""
        self.trigger_manager.fire('app_starting')
        self.do_run()
        self.trigger_manager.fire('app_started')

    def do_run(self):
        """To be overriden in subclass"""
