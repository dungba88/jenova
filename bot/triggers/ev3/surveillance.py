"""Remote controlling EV3"""

import time

from .go import GoBase
from utils.navigation.sweeper import BFSSweeper

class Surveillance(GoBase):
    """class for remote control"""

    sweeper = None

    def run(self, *_):
        """run the action"""
        self.stop()
        self.sweeper = BFSSweeper(SimpleRobot())
        self.sweeper.loggable = True
        self.sweeper.sweep()

    def stop(self):
        """stop both engines"""
        if self.sweeper is not None:
            self.sweeper.stop()

class SimpleRobot(object):
    """simple implementation of robot"""

    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def move(self):
        time.sleep(0.5)
        return True
