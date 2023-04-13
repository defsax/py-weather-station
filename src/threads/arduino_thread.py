from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSlot, QIODevice
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import serial
import time
from helpers import get_t_rh_port, list_serial_devices


class ArduinoHandler(QWidget):
    def __init__(self):
        super(ArduinoHandler, self).__init__()
        self.temp = 0
        self.rh = 0
        self.port = None
        self.serial = None

        self.start_serial()

    def __del__(self):
        print("\nArduino handler unwind.")

        if self.serial:
            print(self.serial)
            self.serial.close()
            print(self.serial)

    def handle_error(self, error):
        if error == QSerialPort.NoError:
            print("serial error:", error)
            return
        print(error, self.serial.errorString())

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
            self.serial.errorOccurred.connect(self.handle_error)

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
                self.rh = float(text.split(",")[0])
                self.temp = float(text.split(",")[1])
                print("serial.canreadline():", self.rh, self.temp)
            except UnicodeDecodeError:
                print("UnicodeDecodeError")
            except:
                print("Other error")
