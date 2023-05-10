import statistics
import yaml

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, QIODevice
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

from pydispatch import dispatcher
from helpers import resource_path


class ArduinoHandler(QWidget):
    def __init__(self):
        super(ArduinoHandler, self).__init__()

        try:
            path = resource_path("settings.yml")
            self.config = yaml.safe_load(open(path))
        except:
            print("Error reading settings.yml")

        self.temp_offset = self.config["temperature_offset"]
        self.temp = 0
        self.temp_history = []

        self.rh_offset = self.config["humidity_offset"]
        self.rh = 0
        self.rh_history = []

        self.port = None
        self.serial = None

        dispatcher.connect(self.set_offset, signal="set_offset", sender=dispatcher.Any)

        self.start_serial()

    def __del__(self):
        print("\nArduino handler unwind.")

        if self.serial:
            print(self.serial)
            self.serial.close()
            print(self.serial)

    def handle_error(self, error):
        # delete function to suppress errors :)
        if error == QSerialPort.NoError:
            print("serial error:", error)
            return
        print("serial error!", error, self.serial.errorString())

    def set_offset(self, sender):
        self.temp_offset = sender["temp_offset"]
        self.rh_offset = sender["hum_offset"]

    @pyqtSlot()
    def start_serial(self):
        serialPortInfoList = QSerialPortInfo.availablePorts()
        for portInfo in serialPortInfoList:
            if "ACM" in portInfo.portName():
                self.port = portInfo.portName()

        if self.port:
            self.serial = QSerialPort(
                self.port, baudRate=QSerialPort.Baud9600, readyRead=self.receive
            )
            self.serial.open(QIODevice.ReadOnly)
            # self.serial.errorOccurred.connect(self.handle_error)

    @pyqtSlot()
    def stop_serial(self):
        if self.serial:
            try:
                self.serial.close()
                self.serial = None

            except:
                print("serial close error")

    def get_data(self):
        return self.port, self.rh, self.temp

    @pyqtSlot()
    def receive(self):
        while self.serial.canReadLine():
            try:
                text = self.serial.readLine().data().decode()
                text = text.rstrip("\r\n")

                rh = float(text.split(",")[0])
                self.rh = rh + self.rh_offset
                self.rh_history.append(self.rh)

                temp = float(text.split(",")[1])
                self.temp = temp + self.temp_offset
                self.temp_history.append(self.temp)

                # send values out
                dispatcher.send(
                    signal="broadcast_serial",
                    sender={
                        "current_humidity": rh,
                        "current_temperature": temp,
                        "offset_h": self.rh_offset,
                        "offset_t": self.temp_offset,
                    },
                )

            except UnicodeDecodeError:
                print("UnicodeDecodeError")
            except:
                print("Other error")

    def getAverageRH(self):
        average = statistics.fmean(self.rh_history)
        self.rh_history = []
        return average

    def getAverageTemp(self):
        average = statistics.fmean(self.temp_history)
        self.temp_history = []
        return average

    def clearAverages(self):
        self.temp_history = []
        self.rh_history = []
