"""ev3 module"""

def is_stopped(state):
    """check if the motor is stopped"""
    return state is not 'running'

def access_large_motors(motors):
    """access large motors"""
    from ev3dev import ev3
    left = ev3.LargeMotor(motors['left'])
    right = ev3.LargeMotor(motors['right'])
    return left, right

def convert_to_pos(motor, rotation):
    """convert rotation to tacho count"""
    return int(rotation * motor.count_per_rot)

def calc_relative_rotation(rotation, left_power, right_power):
    """calibrate the relative rotation with respect to power"""
    max_power = max(abs(left_power), abs(right_power))
    if max_power == 0:
        return 0, 0
    return rotation * left_power / max_power, rotation * right_power / max_power
