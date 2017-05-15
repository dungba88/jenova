"""Module for reading and notifying sensors values"""

import time
import logging
from concurrent.futures import ThreadPoolExecutor

from ev3bot import class_loader

class SensorReadings(object):
    """Sensor readings class"""

    def __init__(self, trigger_manager, app_context):
        self.trigger_manager = trigger_manager
        self.app_context = app_context
        self.running = False

    def run(self):
        """start reading sensors values"""
        if self.running:
            return

        enabled = self.app_context.get_config('ev3.sensors.enabled')
        if not enabled:
            return

        monitors = [
            SensorMonitor(self.trigger_manager, self.app_context)
        ]

        for monitor in monitors:
            monitor.run()

        self.running = True

class SensorMonitor(object):
    """monitor class"""

    logger = logging.getLogger(__name__)

    def __init__(self, trigger_manager, app_context):
        self.trigger_manager = trigger_manager
        self.app_context = app_context
        self.sensor_objects = dict()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.throttle_penalty = 2
        self.throttle_gain = 1
        self.intervals = 0
        self.intervals_min = 0
        self.intervals_max = 0

    def run(self):
        """start monitoring"""
        self.sensor_objects = self.load_sensor_objects()

        if len(self.sensor_objects) == 0:
            return

        self.intervals_min = self.app_context.get_config('ev3.sensors.intervals_min')
        self.intervals_max = self.app_context.get_config('ev3.sensors.intervals_max')
        self.intervals = self.intervals_min

        self.executor.submit(self.monitor)

    def load_sensor_objects(self):
        """load the sensor objects"""
        sensors = self.app_context.get_config('ev3.sensors.monitorables')
        sensor_objects = dict()
        for sensor in sensors:
            if not sensor['enabled']:
                continue
            sensor_obj = class_loader.load_class(sensor['class_name'], address=sensor['port'])
            sensor_objects[sensor['name']] = sensor_obj
        return sensor_objects

    def monitor(self):
        """monitor sensors"""

        while True:
            event = dict()
            for sensor_name in self.sensor_objects:
                sensor_obj = self.sensor_objects[sensor_name]
                sensor_value = self.try_read_sensor(sensor_obj)
                if sensor_value is not None:
                    event[sensor_name] = sensor_value
                    self.gain()
            if len(event) > 0:
                try:
                    self.trigger_manager.fire('sensor_fired', event)
                except Exception as ex:
                    self.logger.error('Uncaught exception when executing trigger: %s', str(ex))
                    self.penalize()

            time.sleep(self.intervals)

    def try_read_sensor(self, sensor):
        """try read sensor value"""
        try:
            return sensor.read_value()
        except Exception as ex:
            msg = 'Uncaught exception when reading sensor %s value: %s'
            self.logger.error(msg, type(sensor).__name__, str(ex))
            self.penalize()

    def gain(self):
        """award when no exception is caught"""
        self.intervals -= self.throttle_gain
        if self.intervals < self.intervals_min:
            self.intervals = self.intervals_min

    def penalize(self):
        """penalize when exception caught"""
        self.intervals += self.throttle_penalty
        if self.intervals > self.intervals_max:
            self.intervals = self.intervals_max
        self.logger.warning('throttling penalized. new intervals: %d', self.intervals)
