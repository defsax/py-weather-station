import weatherhat
import time
from PyQt5.QtCore import QThread

class WeatherThread(QThread):
  def __init__(self):
    super(WeatherThread, self).__init__()
    self.sensors = weatherhat.WeatherHAT()
    self.start()
    
  def run(self):
    while True:
      self.sensors.update(interval=5.0)
      
      if self.sensors.updated_wind_rain:
        print(self.sensors.wind_direction)
        print(self.sensors.wind_speed)
      
      time.sleep(1.0)
