"""Remote controlling EV3"""

from ev3bot.trigger import Trigger

class RemoteControl(Trigger):
    """class for remote control"""

    def run(self, execution_context):
        buttons_pressed = execution_context.event['remote']['buttons_pressed']
        control_behaviors = self.app_context.get_config('ev3.remote_behavior')
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

    def turn_right(self):
        """turn the robot a soft right"""

    def turn_left_back(self):
        """turn the robot a soft left backward"""

    def turn_right_back(self):
        """turn the robot a soft right backward"""

    def skate_up(self):
        """move the robot ahead"""

    def skate_down(self):
        """move the robot backward"""

    def hard_turn_left(self):
        """turn the robot a hard left"""

    def hard_turn_right(self):
        """turn the robot a hard right"""
