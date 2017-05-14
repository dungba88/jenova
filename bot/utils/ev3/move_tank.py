"""move both motor the equally"""

from . import is_stopped, access_large_motors, convert_to_pos

class AbstractMoveTank(object):
    """abstract class for move tank"""
    def __init__(self, motors):
        self.left, self.right = access_large_motors(motors)

    def run(self, **kwargs):
        """run the robot"""
        self.left.speed_sp = kwargs['left_power'] * 10
        self.right.speed_sp = kwargs['right_power'] * 10

        if 'stop_action' not in kwargs:
            kwargs['stop_action'] = 'brake'

        self.left.stop_action = self.right.stop_action = kwargs['stop_action']

        self.do_run(**kwargs)

        self.left.wait(is_stopped)
        self.right.wait(is_stopped)

    def do_run(self, **kwargs):
        """run the actual command"""

class TimedMoveTank(AbstractMoveTank):
    """class for move by timed period"""

    def do_run(self, **kwargs):
        time_sp = kwargs['time']*1000
        self.left.run_timed(time_sp=time_sp)
        self.right.run_timed(time_sp=time_sp)

class RotationMoveTank(AbstractMoveTank):
    """class for move by rotation"""

    def do_run(self, **kwargs):
        rotation = kwargs['rotation']
        self.left.run_to_rel_pos(position_sp=convert_to_pos(self.left, rotation))
        self.right.run_to_rel_pos(position_sp=convert_to_pos(self.right, rotation))

class DegreeMoveTank(AbstractMoveTank):
    """class for move by rotation"""

    def do_run(self, **kwargs):
        rotation = kwargs['degree'] / 180
        self.left.run_to_rel_pos(position_sp=convert_to_pos(self.left, rotation))
        self.right.run_to_rel_pos(position_sp=convert_to_pos(self.right, rotation))
