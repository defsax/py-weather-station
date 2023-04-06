import time
from pydispatch import dispatcher
from PyQt5.QtCore import QThread, pyqtSignal

from threads.light_thread import LightThread
from threads.weather_thread import WeatherThread
from threads.arduino_thread import ArduinoHandler

from helpers import get_t_rh_port, set_sensor_status

class SensorManager(QThread):
  set_sensor_status = pyqtSignal(str, str, str)
  def __init__(self):
    super(SensorManager, self).__init__()        
    self.set_sensor_status.connect(set_sensor_status)
    # ~ port = get_t_rh_port()
    
    self.light_thread = LightThread()
    # ~ self.weather_thread = WeatherThread()
    self.t_rh_thread = ArduinoHandler()
    # ~ self.t_rh_thread.start_serial(get_t_rh_port())
    
    self.start()
    # ~ self.sensors = []
  
  def check_temp_humidity(self):
    port = get_t_rh_port()
    # ~ print(self.t_rh_thread.serial.QSerialPortInfo())
    
    if port != "":
      # ~ print("Temperature/RH sensor connected.")
      self.set_sensor_status.emit("temp_rh", "Connected", "green")
      
      # ~ self.t_rh_thread.serial.setPort(port)
      # start serial port if not already started
      # ~ if self.t_rh_thread.serial == None:
        # ~ self.t_rh_thread.start_serial(port)
        
    else:
      # ~ print("Temperature/RH sensor disconnected.")
      self.set_sensor_status.emit("temp_rh", "Disconnected", "red")
      
      # close serial port if not already closed
      # ~ if self.t_rh_thread.serial != None:
        # ~ self.t_rh_thread.stop_serial()
    
  def check_light(self):
    if self.light_thread.is_attached == False:
      # ~ print("Light sensor disconnected. Trying to connect...")
      self.set_sensor_status.emit("light", "Disconnected", "red")
      try:
        self.light_thread.light_sensor.openWaitForAttachment(1000)
      except:
        print("Unable to connect light sensor...")
    else:
      # ~ print("Light sensor connected.")
      self.set_sensor_status.emit("light", "Connected", "green")
  
  def check_wind(self):
    wind_direction_cardinal = self.weather_thread.sensors.degrees_to_cardinal(self.weather_thread.sensors.wind_direction)
    print("wind dir: ", wind_direction_cardinal)
    print("wind dir: ", self.weather_thread.sensors.wind_direction)
    print("wind speed: ", self.weather_thread.sensors.wind_speed)
    print("temperature: ", self.weather_thread.sensors.temperature)
    
    if self.weather_thread.sensors.updated_wind_rain:
      print(self.weather_thread.sensors.wind_direction)
      print(self.weather_thread.sensors.wind_speed)
      
  
  def run(self):    
    while True:   
      # ~ print("Checking for sensors...")
      self.check_temp_humidity()
      self.check_light()
      # ~ print("\narduino serial", self.t_rh_thread.get_data(), self.t_rh_thread.serial)
      # ~ self.check_wind()
      time.sleep(5)
