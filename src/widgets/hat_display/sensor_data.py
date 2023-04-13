import math
import weatherhat
from weatherhat import history


class SensorData:
    def __init__(self, sensor_manager):
        self.sensor = sensor_manager

        self.temperature = history.History()

        self.pressure = history.History()

        self.humidity = history.History()
        self.relative_humidity = history.History()
        self.dewpoint = history.History()

        self.lux = history.History()

        self.wind_speed = history.WindSpeedHistory()
        self.wind_direction = history.WindDirectionHistory()

        self.rain_mm_sec = history.History()
        self.rain_total = 0

        # Track previous average values to give the compass a trail
        self.needle_trail = []

        self.AVERAGE_SAMPLES = 120
        self.WIND_DIRECTION_AVERAGE_SAMPLES = 60
        self.COMPASS_TRAIL_SIZE = 120

        # We can compensate for the heat of the Pi and other environmental conditions using a simple offset.
        # Change this number to adjust temperature compensation!
        self.OFFSET = -7.5

    def update(self, interval=5.0):
        self.sensor.temperature_offset = self.OFFSET
        # ~ self.sensor.update(interval)
        try:
            self.sensor.t_rh_thread

            self.temperature.append(self.sensor.t_rh_thread.temp)
            self.relative_humidity.append(self.sensor.t_rh_thread.rh)

        except:
            print("temp rh sensor thread disconnected")
            # self.temperature.append(self.sensor.t_rh_thread.temp)
            # self.relative_humidity.append(self.sensor.t_rh_thread.rh)

        # ~ if self.sensor.updated_wind_rain:
        # ~ self.rain_total = self.sensor.rain_total
        # ~ else:
        # ~ self.rain_total = 0
        self.lux.append(round(self.sensor.light_thread.wm2, 4))
        self.wind_speed.append(round(self.sensor.wind_speed, 4))
        self.wind_direction.append(self.sensor.wind_dir)

        # ~ self.rain_mm_sec.append(self.sensor.rain)

        # ~ self.needle = math.radians(self.wind_direction.average(self.WIND_DIRECTION_AVERAGE_SAMPLES))
        # ~ self.needle_trail.append(self.needle)
        # ~ self.needle_trail = self.needle_trail[-self.COMPASS_TRAIL_SIZE:]
