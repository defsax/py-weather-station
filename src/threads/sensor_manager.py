import time
from pydispatch import dispatcher
from PyQt5.QtCore import QThread, pyqtSignal

from threads.light_thread import LightThread
from threads.weather_thread import WeatherThread

from helpers import get_temp_port, set_sensor_status

class SensorManager(QThread):
  set_sensor_status = pyqtSignal(str, str, str)
  def __init__(self):
    super(SensorManager, self).__init__()        
    self.set_sensor_status.connect(set_sensor_status)
    self.light_thread = LightThread()
    self.weather_thread = WeatherThread()
    self.start()
    # ~ self.sensors = []
  
  def check_temp_humidity(self):
    port = get_temp_port()
    
    if port != "":
      print("Temperature/RH sensor connected.")
      self.set_sensor_status.emit("temp_rh", "Connected", "green")
    else:
      print("Temperature/RH sensor disconnected.")
      self.set_sensor_status.emit("temp_rh", "Disconnected", "red")
    
  def check_light(self):
    if self.light_thread.is_attached == False:
      print("Light sensor disconnected. Trying to connect...")
      self.set_sensor_status.emit("light", "Disconnected", "red")
      try:
        self.light_thread.light_sensor.openWaitForAttachment(1000)
      except:
        print("Unable to connect light sensor...")
    else:
      print("Light sensor connected.")
      self.set_sensor_status.emit("light", "Connected", "green")
  
  def check_wind(self):
    print(self.weather_thread.sensors.wind_direction)
    print(self.weather_thread.sensors.wind_speed)
    print(self.weather_thread.sensors.temperature)
    
    if self.weather_thread.sensors.updated_wind_rain:
      print(self.weather_thread.sensors.wind_direction)
      print(self.weather_thread.sensors.wind_speed)
      
  
  def run(self):    
    while True:   
      print("Checking for sensors...")
      self.check_temp_humidity()
      self.check_light()
      self.check_wind()
      time.sleep(5)
