"""Remote controlling EV3"""

from utils.ev3.sensors.infrared import InfraredSensorReadings
from utils.navigation.sweeper import BFSSweeper
from .go import GoEV3

class Surveillance(object):
    """class for remote control"""

    sweeper = None

    def run(self, _, app_context):
        """run the action"""
        power = app_context.get_config('ev3.remote.power')
        motors = app_context.get_config('ev3.motors.wheels')
        sensors = app_context.get_config('ev3.sensors.monitorables')
        infrared_sensor = self.find_infrared(sensors)

        self.stop()
        self.sweeper = BFSSweeper(SimpleRobot(power, motors, infrared_sensor['port']))
        self.sweeper.loggable = True
        self.sweeper.sweep()

    def stop(self):
        """stop both engines"""
        if self.sweeper is not None:
            self.sweeper.stop()

    def find_infrared(self, sensors):
        """find the infrared sensor config"""
        for sensor in sensors:
            if sensor['name'] == 'infrared':
                return sensor
        return None

class SimpleRobot(object):
    """simple implementation of robot"""

    def __init__(self, power, motors, infrared_port):
        self.power = power
        self.controller = GoEV3()
        self.controller.time = 0.5
        self.controller.motors = motors
        self.infrared_reader = InfraredSensorReadings(infrared_port)

    def turn_left(self):
        self.controller.turn_left(self.power)
        return True

    def turn_right(self):
        self.controller.turn_right(self.power)
        return True

    def move(self):
        infrared_readings = self.infrared_reader.read_value()
        if infrared_readings['proximity'] < 0.5:
            return False
        self.controller.skate_up(self.power)
        return True
