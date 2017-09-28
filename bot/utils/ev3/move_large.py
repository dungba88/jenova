"""move both motor the equally"""

from . import convert_to_pos

class AbstractMoveLarge(object):
    """abstract class for move tank"""
    def __init__(self, port):
        from ev3dev import ev3
        self.motor = ev3.LargeMotor(port)

    def run(self, **kwargs):
        """run the robot"""
        self.motor.speed_sp = kwargs['power'] * 10

        self.do_run(**kwargs)

    def do_run(self, **kwargs):
        """run the actual command"""

class ForeverMoveLarge(AbstractMoveLarge):
    """class for move by timed period"""

    def do_run(self, **kwargs):
        self.motor.run_forever()

class TimedMoveLarge(AbstractMoveLarge):
    """class for move by timed period"""

    def do_run(self, **kwargs):
        time_sp = kwargs['time']*1000
        self.motor.run_timed(time_sp=time_sp)

class RotationMoveLarge(AbstractMoveLarge):
    """class for move by rotation"""

    def do_run(self, **kwargs):
        rot = kwargs['rotation']
        if self.motor.speed_sp < 0:
            rot = -rot
        self.motor.run_to_rel_pos(position_sp=convert_to_pos(self.motor, rot))

class DegreeMoveLarge(AbstractMoveLarge):
    """class for move by rotation"""

    def do_run(self, **kwargs):
        rot = kwargs['degree'] / 180
        if self.motor.speed_sp < 0:
            rot = -rot
        self.motor.run_to_rel_pos(position_sp=convert_to_pos(self.motor, rot))
