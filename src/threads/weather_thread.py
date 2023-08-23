import time
import weatherhat
from PyQt5.QtCore import QThread, pyqtSignal


class WeatherThread(QThread):
    set_wind = pyqtSignal(str, float)

    def __init__(self):
        super(WeatherThread, self).__init__()
        self.sensors = weatherhat.WeatherHAT()
        self.start()

    def run(self):
        while True:
            self.sensors.update(interval=5.0)

            if self.sensors.updated_wind_rain:
                wind_direction_cardinal = self.sensors.degrees_to_cardinal(
                    self.sensors.wind_direction
                )
                wind_speed = self.sensors.wind_speed

                self.set_wind.emit(wind_direction_cardinal, wind_speed)
                if wind_speed == 0.0 and wind_direction_cardinal[0] == "E":
                    self.sensors.reset_counts()
                    print("Weatherhat lost, restarting weatherhat")
                    # continue

            time.sleep(1.0)
