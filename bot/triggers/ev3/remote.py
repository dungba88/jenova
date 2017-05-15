"""Remote controlling EV3"""

from .go import GoBase

class RemoteControl(GoBase):
    """class for remote control"""

    power = 100
    run_flag = False

    def run(self, execution_context):
        self.motors = self.app_context.get_config('ev3.motors.wheels')

        buttons_pressed = execution_context.event['remote']['buttons_pressed']
        power = self.app_context.get_config('ev3.remote.power')
        control_behaviors = self.app_context.get_config('ev3.remote.behavior')

        for behavior in control_behaviors:
            if set(buttons_pressed) == set(control_behaviors[behavior]):
                execution_context.finish(behavior)
                self.run_behavior(behavior, power)
                break
        else:
            execution_context.finish(control_behaviors['default'])
            self.run_behavior(control_behaviors['default'], power)

    def stop(self):
        if not self.run_flag:
            return
        from ev3dev import ev3
        ev3.LargeMotor(self.motors['left']).stop()
        ev3.LargeMotor(self.motors['right']).stop()
        self.run_flag = False

    def run_motor(self, motor, power):
        """run a large motor"""
        self.run_flag = True
        super.run_motor(motor, power)
