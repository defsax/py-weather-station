from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from datetime import datetime

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget

class LightThread(QWidget):
  # set up pyqtsignal
  # ~ set_time = pyqtSignal(str)
  
  def __init__(self):
    super(LightThread, self).__init__()
  
    self.voltage = 0
    self.wm2 = 0
  
    self.light_sensor = VoltageInput()
    self.light_sensor.setChannel(1)
    
    self.light_sensor.setOnVoltageChangeHandler(self.onVoltageChange)
    self.light_sensor.setOnAttachHandler(self.onAttachHandler)
    self.light_sensor.setOnDetachHandler(self.onDetachHandler)
    try:
      self.light_sensor.openWaitForAttachment(1000)
      self.is_attached = True
    except:
      self.is_attached = False
  
  def __del__(self):
    print("Light sensor close.")
    self.light_sensor.close()

  def onAttachHandler(self, phidget_handle):
    # ~ print("Light sensor Attached!", phidget_handle)    
    self.is_attached = True
    
  def onDetachHandler(self, phidget_handle):
    # ~ print("Light sensor Detached!", phidget_handle)
    self.is_attached = False

  def onVoltageChange(self, phidget_handle, voltage):
    self.voltage = voltage
    self.wm2 = 0.4 * voltage * 1000
    # ~ print("Voltage: " + str(self.voltage) + "\t\tW m^2: " + str(self.wm2))
