from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *


from pydispatch import dispatcher
from PyQt5.QtWidgets import QWidget


class PhidgetThread(QWidget):
    # set up pyqtsignal
    # ~ set_time = pyqtSignal(str)

    def __init__(self):
        super(PhidgetThread, self).__init__()

        self.wm2 = 0
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
        # print(
        #     "Voltage: "
        #     + str(self.light_voltage_reading)
        #     + "\t\tW m^2: "
        #     + str(self.wm2)
        # )

        # send values out
        dispatcher.send(
            signal="broadcast_light",
            sender={"wm2": self.wm2},
        )

    def onBatteryVoltageChange(self, phidget_handle, voltage):
        self.battery_voltage_reading = voltage * 3.03
        # print("Battery voltage: " + str(self.battery_voltage_reading))

        # send values out
        dispatcher.send(
            signal="broadcast_battery",
            sender={"voltage": self.battery_voltage_reading},
        )
