"""Remote controlling EV3"""

import time

from utils.ev3.sensors.infrared import InfraredSensorReadings
from utils.navigation.sweeper import BFSSweeper
from .go import GoBase

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
        self.sweeper = BFSSweeper(SimpleRobot(25, motors, infrared_sensor['port']))
        self.sweeper.spiral = False
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

from utils.ev3 import move_large

class SurveillanceGo(GoBase):

    def run_motor(self, motor, power):
        move_large.RotationMoveLarge(self.motors[motor]).run(power=power, rotation=1.25)

class SimpleRobot(object):
    """simple implementation of robot"""

    def __init__(self, power, motors, infrared_port):
        self.power = power
        self.controller = SurveillanceGo()
        self.controller.motors = motors
        self.infrared_reader = InfraredSensorReadings(infrared_port)

    def turn_left(self):
        self.controller.hard_turn_left(self.power)
        time.sleep(2)
        return True

    def turn_right(self):
        self.controller.hard_turn_right(self.power)
        time.sleep(2)
        return True

    def move(self):
        infrared_readings = self.infrared_reader.read_value()
        print(infrared_readings['proximity'])
        if infrared_readings['proximity'] < 30:
            print('walled')
            return False
        self.controller.skate_up(self.power)
        time.sleep(2)
        return True
