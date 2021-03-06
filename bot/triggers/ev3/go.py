"""Trigger to make the bot go"""

from utils.ev3 import move_large

class GoBase(object):
    """Base class for make EV3 go"""
    motors = None

    def run_behavior(self, behavior, power):
        """run the behavior"""
        getattr(self, behavior)(power)

    def turn_left(self, power):
        """turn the robot a soft left"""
        self.run_motor('left', 0)
        self.run_motor('right', power)

    def turn_right(self, power):
        """turn the robot a soft right"""
        self.run_motor('left', power)
        self.run_motor('right', 0)

    def turn_left_back(self, power):
        """turn the robot a soft left backward"""
        self.run_motor('left', 0)
        self.run_motor('right', -power)

    def turn_right_back(self, power):
        """turn the robot a soft right backward"""
        self.run_motor('left', -power)
        self.run_motor('right', 0)

    def skate_up(self, power):
        """move the robot ahead"""
        self.run_motor('left', power)
        self.run_motor('right', power)

    def skate_down(self, power):
        """move the robot backward"""
        self.run_motor('left', -power)
        self.run_motor('right', -power)

    def hard_turn_left(self, power):
        """turn the robot a hard left"""
        self.run_motor('left', -power)
        self.run_motor('right', power)

    def hard_turn_right(self, power):
        """turn the robot a hard right"""
        self.run_motor('left', power)
        self.run_motor('right', -power)

    def run_motor(self, motor, power):
        """run a large motor"""
        move_large.ForeverMoveLarge(self.motors[motor]).run(power=power)

class GoEV3(GoBase):
    """class for remote control"""
    time = 1

    def run(self, execution_context, app_context):
        """run the action"""
        self.motors = app_context.get_config('ev3.motors.wheels')
        power = execution_context.event['power']
        behavior = execution_context.event['behavior']
        execution_context.finish(behavior)
        self.time = execution_context.event['time']
        self.run_behavior(behavior, power)

    def run_motor(self, motor, power):
        """run a large motor"""
        move_large.TimedMoveLarge(self.motors[motor]).run(time=self.time, power=power)
