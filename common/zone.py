#!/usr/bin/env python

from common.relay import Relay
from common.temp_sensor import TempSensor
from common.rc_sensor import RcSensor
from common.temp_sensor import TempSensor
import time

class Zone (object):

    def __init__(self, alias=None, moisture_sensor_gpio=None, relay_gpio=None, moisture_water_threshold=None, watering_duration=None, min_seconds_between_waterings=18000, temp_sensor_id=None):
        self.alias = alias
        self._moisture_sensor_gpio = moisture_sensor_gpio
        self.moisture_sensor = RcSensor(self._moisture_sensor_gpio)
        self._relay_gpio = relay_gpio
        self.moisture_water_threshold = moisture_water_threshold
        self.watering_duration = watering_duration
        self.min_seconds_between_waterings = min_seconds_between_waterings
        self._temp_sensor_id = temp_sensor_id
        self.temp_sensor = TempSensor(self._temp_sensor_id)
        self.relay = Relay(self._relay_gpio)
        self.last_water_time = None

    def water(self):
        now = time.time()
        if self.last_water_time is None:
            self.last_water_time = time.time()
        elif now - self.last_water_time <= self.min_seconds_between_waterings:
            return
        else:
            self.last_water_time = now
            self.relay.set_state(self.relay.ON)
            time.sleep(self.watering_duration)
            self.relay.set_state(self.relay.OFF)

    def water_now(self):
        self.last_water_time = time.time()
        self.relay.set_state(self.relay.ON)
        time.sleep(self.watering_duration)
        self.relay.set_state(self.relay.OFF)

    @property
    def temp(self):
        assert isinstance(self.temp_sensor, TempSensor)
        return self.temp_sensor.get_f()

    @property
    def moisture(self):
        return self.moisture_sensor.rc_count()
