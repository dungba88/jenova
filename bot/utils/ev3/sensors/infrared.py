"""infrared sensor"""

class InfraredSensorReadings(object):
    """class for accessing infrared sensor"""
    def __init__(self, address):
        from ev3dev.core import InfraredSensor
        self.sensor = InfraredSensor(address=address)

    def read_value(self):
        """read the sensor value"""
        return {
            'proximity': self.sensor.proximity,
            'raw_value': self.sensor.value
        }
