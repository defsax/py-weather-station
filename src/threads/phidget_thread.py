import statistics

from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *

from PyQt5.QtWidgets import QWidget

from dispatcher.senders import update_light, update_voltage


class PhidgetThread(QWidget):
    # set up pyqtsignal
    # ~ set_time = pyqtSignal(str)

    def __init__(self):
        super(PhidgetThread, self).__init__()

        self.wm2 = 0
        self.wm2_history = []
        self.light_voltage_reading = 0
        self.light_sensor = VoltageInput()
        self.light_sensor.setChannel(1)

        self.battery_voltage_reading = 0
        self.battery_voltage = VoltageInput()
        self.battery_voltage.setChannel(0)

        self.light_sensor.setOnVoltageChangeHandler(self.onLightVoltageChange)
        self.battery_voltage.setOnVoltageChangeHandler(self.onBatteryVoltageChange)

        self.light_sensor.setOnAttachHandler(self.onAttachHandler)
        self.light_sensor.setOnDetachHandler(self.onDetachHandler)
        try:
            self.light_sensor.openWaitForAttachment(1000)
            self.battery_voltage.openWaitForAttachment(1000)
            self.is_attached = True
        except:
            self.is_attached = False

    def __del__(self):
        print("Light sensor close.")
        self.light_sensor.close()

    def onAttachHandler(self, phidget_handle):
        print("Light sensor Attached!", phidget_handle)
        self.is_attached = True

    def onDetachHandler(self, phidget_handle):
        print("Light sensor Detached!", phidget_handle)
        self.is_attached = False

    def onLightVoltageChange(self, phidget_handle, voltage):
        self.light_voltage_reading = voltage
        self.wm2 = 0.4 * voltage * 1000
        self.wm2_history.append(self.wm2)
        update_light(self.wm2)

    def getAverageLight(self):
        average = statistics.fmean(self.wm2_history)
        self.wm2_history = []
        return average

    def onBatteryVoltageChange(self, phidget_handle, voltage):
        self.battery_voltage_reading = voltage * 3.03
        update_voltage(self.battery_voltage_reading)

    def clearAverages(self):
        self.wm2_history = []
