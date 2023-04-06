from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSlot, QIODevice
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import serial
import time
from helpers import get_t_rh_port

class ArduinoHandler(QThread):
  def __init__(self):
    super(ArduinoHandler, self).__init__()        
    self.temp = 0
    self.rh = 0
    self.port = None
    self.serial = None
    
    # ~ self.init_serial(port)
    print(QSerialPortInfo.availablePorts())
    
    self.start_serial()
    self.start()
  
  def start_serial(self):
    port = get_t_rh_port()
    print("serial port:", port)
    
    if port:
      self.port = port
      self.serial = QSerialPort(
        port,
        baudRate = QSerialPort.Baud9600,
        readyRead = self.receive
      )
      self.serial.open(QIODevice.ReadOnly)
      
  def stop_serial(self):
    try:
      self.serial.close()
      self.serial = None
      self.port = None
      self.temp = 0
      self.rh = 0
    except:
      print("could not close serial")
    
  def get_data(self):
    return self.port, self.rh, self.temp

  @pyqtSlot()
  def receive(self):
    print("rh, temp:", self.rh, self.temp)
    while self.serial.canReadLine():
      try:
        text = self.serial.readLine().data().decode()
        text = text.rstrip('\r\n')
        self.rh = text.split(",")[0]
        self.temp = text.split(",")[1]
        print("serial.canreadline():", self.rh, self.temp)
      except UnicodeDecodeError:
        print("UnicodeDecodeError")
      except:
        print("Other error")
        
  def run(self):     
    while True:
      print("arduino thread", self.temp, self.rh)
      port = get_t_rh_port()
      if port != "":
        # ~ print("Temperature/RH sensor connected.")
        # ~ self.set_sensor_status.emit("temp_rh", "Connected", "green")
        
        # ~ self.t_rh_thread.serial.setPort(port)
        # start serial port if not already started
        if self.serial == None:
          self.start_serial()
        
      else:
        # ~ print("Temperature/RH sensor disconnected.")
        # ~ self.set_sensor_status.emit("temp_rh", "Disconnected", "red")
        
        # close serial port if not already closed
        if self.serial != None:
          self.stop_serial()
      time.sleep(5)

