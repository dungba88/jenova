"""Remote controlling EV3"""

from ev3bot.trigger import Trigger

from utils.ev3 import move_large

class RemoteControl(Trigger):
    """class for remote control"""

    motors = None
    power = 100

    def run(self, execution_context):
        self.motors = self.app_context.get_config('ev3.motors.wheels')
        self.power = self.app_context.get_config('ev3.remote.power')

        buttons_pressed = execution_context.event['remote']['buttons_pressed']
        control_behaviors = self.app_context.get_config('ev3.remote.behavior')
        for behavior in control_behaviors:
            if set(buttons_pressed) == set(control_behaviors[behavior]):
                self.run_behavior(behavior)

    def run_behavior(self, behavior):
        """run the behavior"""
        getattr(self, behavior)()

    def beacon(self):
        """run when beacon is clicked"""

    def turn_left(self):
        """turn the robot a soft left"""
        self.run_motor('left', 0)
        self.run_motor('right', self.power)

    def turn_right(self):
        """turn the robot a soft right"""
        self.run_motor('left', self.power)
        self.run_motor('right', 0)

    def turn_left_back(self):
        """turn the robot a soft left backward"""
        self.run_motor('left', 0)
        self.run_motor('right', -self.power)

    def turn_right_back(self):
        """turn the robot a soft right backward"""
        self.run_motor('left', -self.power)
        self.run_motor('right', 0)

    def skate_up(self):
        """move the robot ahead"""
        self.run_motor('left', self.power)
        self.run_motor('right', self.power)

    def skate_down(self):
        """move the robot backward"""
        self.run_motor('left', -self.power)
        self.run_motor('right', -self.power)

    def hard_turn_left(self):
        """turn the robot a hard left"""
        self.run_motor('left', -self.power)
        self.run_motor('right', self.power)

    def hard_turn_right(self):
        """turn the robot a hard right"""
        self.run_motor('left', self.power)
        self.run_motor('right', -self.power)

    def run_motor(self, motor, power):
        """run a large motor"""
        move_large.ForeverMoveLarge(self.motors[motor]).run(power=power)
        