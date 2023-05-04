from weatherhat import history


class SensorData:
    def __init__(self, sensor_manager):
        self.sensor = sensor_manager

        self.battery_voltage = history.History()

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
        try:
            self.sensor.t_rh_thread

            self.temperature.append(self.sensor.t_rh_thread.temp)
            self.relative_humidity.append(self.sensor.t_rh_thread.rh)

        except:
            print("temp rh sensor thread disconnected")

        self.lux.append(round(self.sensor.phidget_thread.wm2, 4))
        self.wind_speed.append(round(self.sensor.wind_speed, 4))

        # format for just first letters of wind direction
        wd = [s[0] for s in self.sensor.wind_dir.split()]
        d = "".join(wd)
        self.wind_direction.append(d)

        self.battery_voltage.append(self.sensor.phidget_thread.battery_voltage_reading)
