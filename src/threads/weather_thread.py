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
      time.sleep(1.0)
