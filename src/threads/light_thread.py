from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal

class LightThread(QWidget):
  # set up pyqtsignal
  # ~ set_time = pyqtSignal(str)
  
  def __init__(self):
    super(LightThread, self).__init__()
    

    # ~ def main():
    voltageInput1 = VoltageInput()
    voltageInput1.setChannel(1)
    voltageInput1.setOnVoltageChangeHandler(onVoltageChange)
    voltageInput1.openWaitForAttachment(5000)
    
    try:
      input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
      pass

    voltageInput1.close()
    # ~ main()

  def onVoltageChange(self, voltage):
    # ~ print("Voltage [" + str(self.getChannel()) + "]: " + str(0.4 * voltage * 1000))
    print("Voltage [" + str(self.getChannel()) + "]: " + str(voltage))

  def run(self):     
    # ~ while True:
      # ~ # get input
      # ~ adc = ioe.input(input_pin)
      # ~ vref = ioe.get_adc_vref()
      # ~ print(vref)
      # ~ adc = round(adc, 4)
      

      # ~ if adc != last_adc:
        # ~ light = 0.4 * adc * 1000
        # ~ print(str(round(light, 4)) + "Wm^2")
        # ~ print("{:.4f}v\n".format(adc))
        # ~ last_adc = adc
        
        # ~ # wm^2 = 0.4 * adc * 1000

      # ~ time.sleep(1)
