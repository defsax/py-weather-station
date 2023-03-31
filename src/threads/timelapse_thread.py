from threading import Event
import signal
import time
from PyQt5.QtCore import QThread, pyqtSignal

class TimelapseThread(QThread):
  def __init__(self, sensors):
    super(TimelapseThread, self).__init__()
    self.sensors = sensors
    
  def setup(self):
    print("timelapse thread setup")
    self.exit_flag = Event()
  
  def check_sensor(self, arg):
    print("check sensor", arg)
    
  def log_data(self):
    # log temp and rh for each sensor          
    for i, sensor in enumerate(self.sensors):
      port, rh, temp = sensor.get_data()
      print("logging:", temp, rh)
      # ~ try:
        # ~ start = datetime.now()
        # ~ date_time = start.strftime("%m-%d-%Y_%H-%M-%S")
        # ~ print(self.path)
        # ~ with open(self.path + "/data.txt", "a") as f:
          # ~ f.write(date_time + ",")
          # ~ f.write(rh + ",")
          # ~ f.write(temp + ",")
          # ~ f.write("img" + str(count).zfill(4)+".png\n")
          # ~ f.close()
      # ~ except:
        # ~ print("error")
 
  
  def run(self):    
    while not self.exit_flag.wait(timeout=5):
      self.check_sensor("args")
      self.log_data()

    
  def stop(self):
    print("Timelapse thread stopping...")
    self.exit_flag.set()
    
