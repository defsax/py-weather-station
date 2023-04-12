from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSlot, QIODevice
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import serial
import time
from helpers import get_t_rh_port

class ArduinoHandler(QWidget):
  def __init__(self):
    super(ArduinoHandler, self).__init__()        
    self.temp = 0
    self.rh = 0
    self.port = None
    self.serial = None
    
    # ~ self.init_serial(port)
    print("available ports:")
    serialPortInfos = QSerialPortInfo.availablePorts()
    for portInfo in serialPortInfos:
      print(portInfo.portName())
    
    self.start_serial()
  
  def __del__(self):
    print("\nArduino handler unwind.")
    
    if self.serial:
      print(self.serial)
      self.serial.close()
      print(self.serial)
  
  def handle_error(self, error):
    if error == QSerialPort.NoError:
      print(error)
      return
    print(error, self.serial_port.errorString())
  
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
      self.serial.errorOccurred.connect(self.handle_error)

    
  def get_data(self):
    return self.port, self.rh, self.temp

  @pyqtSlot()
  def receive(self):
    # ~ print("rh, temp:", self.rh, self.temp)
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
        
 
