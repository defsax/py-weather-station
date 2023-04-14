from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSlot, QIODevice
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import yaml
from pydispatch import dispatcher


class ArduinoHandler(QWidget):
    def __init__(self):
        super(ArduinoHandler, self).__init__()
        try:
            self.config = yaml.safe_load(
                open("/home/pi/code/python/py-weather-station/settings.yml")
            )
        except:
            print("Error reading settings.yml")

        self.temp_offset = self.config["temperature_offset"]
        self.temp = 0
        self.rh_offset = self.config["humidity_offset"]
        self.rh = 0

        self.port = None
        self.serial = None

        dispatcher.connect(self.set_offset, signal="set_offset", sender=dispatcher.Any)

        self.start_serial()

    def set_offset(self, sender):
        self.temp_offset = sender["temp_offset"]
        self.rh_offset = sender["hum_offset"]
        print(sender)

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
                # print(
                #     "\nhumidity:",
                #     text.split(",")[0],
                #     "offset:",
                #     self.rh_offset,
                #     "humidity with offset:",
                #     self.rh,
                # )
                temp = float(text.split(",")[1])
                self.temp = temp + self.temp_offset
                # print(
                #     "temperature:",
                #     text.split(",")[1],
                #     "offset:",
                #     self.temp_offset,
                #     "temperature with offset:",
                #     self.temp,
                # )
                # send values out
                print("temp:", temp)
                dispatcher.send(
                    signal="broadcast_serial",
                    sender={"current_humidity": rh, "current_temperature": temp},
                )

                # print("serial.canreadline():", self.rh, self.temp)
            except UnicodeDecodeError:
                print("UnicodeDecodeError")
            except:
                print("Other error")
