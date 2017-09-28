"""remote controller"""

class RemoteControlReadings(object):
    """class for accessing remote controller"""
    def __init__(self, address):
        from ev3dev.core import RemoteControl, InfraredSensor
        self.sensor = RemoteControl(InfraredSensor(address=address))

    def read_value(self):
        """read the sensor value"""
        return {
            'buttons_pressed': self.sensor.buttons_pressed,
            'sensor': self.sensor
        }
