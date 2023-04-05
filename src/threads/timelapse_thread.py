from threading import Event
from datetime import datetime
import signal
import time
import os
from PyQt5.QtCore import QThread, pyqtSignal

# ~ import weatherhat
from threads.sensor_manager import SensorManager

class TimelapseThread(QThread):
  def __init__(self, sensors):
    super(TimelapseThread, self).__init__()
    self.sensor_manager = SensorManager()
    self.sensors = sensors
    # ~ self.weatherhat_sensors = weatherhat.WeatherHAT()
    
  def setup(self):
    print("timelapse thread setup")
    
    # get/set destination folder
    self.path = os.path.abspath("/home/pi/weather_station_data")

    # get and format date
    start = datetime.now()
    self.start_time = start.strftime("%m-%d-%Y_%H-%M-%S")

    # create file with mission id and date
    self.file_name = "/test_" + self.start_time + ".csv"

    # write defaults (csv)
    try:
      with open(self.path + self.file_name, "a") as f:
        f.write("time,humidity,temperature,pressure,light,wind_speed,wind_dir\n")
        f.close()
    except:
      print("write setup error")
    
    self.exit_flag = Event()
  
  def check_sensor(self, arg):
    print("check sensor", arg)
    
  def log_data(self):
    # ~ self.weatherhat_sensors.update(interval=60.0)
    # ~ print(self.weatherhat_sensors.temperature)
    
    
    # log temp and rh for each sensor          
    for i, sensor in enumerate(self.sensors):
      print(i, sensor)
      port, rh, temp = sensor.get_data()
      print("logging:", temp, rh)
      
      try:
        t = datetime.now()
        date_time = t.strftime("%m-%d-%Y_%H-%M-%S")
        print(self.path)
        with open(self.path + self.file_name, "a") as f:
          f.write(date_time + ",")
          f.write(rh + ",")
          f.write(temp + ",")
          f.write("\n")
          f.close()
      except:
        print("write error")
 
  
  def run(self):    
    while not self.exit_flag.wait(timeout=5):
      self.check_sensor("args")
      self.log_data()

    
  def stop(self):
    print("Timelapse thread stopping...")
    self.exit_flag.set()
    
