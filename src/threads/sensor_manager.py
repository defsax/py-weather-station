import time
import statistics
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtSerialPort import QSerialPortInfo

from threads.phidget_thread import PhidgetThread
from threads.weather_thread import WeatherThread
from threads.arduino_thread import ArduinoHandler

from helpers import set_sensor_status
from pydispatch import dispatcher


class SensorManager(QThread):
    set_sensor_status = pyqtSignal(str, str, str)
    start_sensor = pyqtSignal()
    stop_sensor = pyqtSignal()

    def __init__(self):
        super(SensorManager, self).__init__()
        self.set_sensor_status.connect(set_sensor_status)
        # ~ port = get_t_rh_port()

        self.phidget_thread = PhidgetThread()
        self.weather_thread = WeatherThread()
        self.weather_thread.set_wind.connect(self.set_wind)
        self.t_rh_thread = ArduinoHandler()
        self.start_sensor.connect(self.t_rh_thread.start_serial)
        self.stop_sensor.connect(self.t_rh_thread.stop_serial)

        self.wind_speed = 0
        self.wind_speed_history = []
        self.wind_dir = ""

        self.start()

    def check_temp_humidity(self):
        # port = list_serial_devices()
        self.port = ""
        serialPortInfoList = QSerialPortInfo.availablePorts()
        for portInfo in serialPortInfoList:
            if "ACM" in portInfo.portName():
                self.port = portInfo.portName()

        if self.port != "":
            # print("Temperature/RH sensor connected.")
            self.set_sensor_status.emit("temp_rh", "Connected", "green")

            # start serial port if not already started
            if self.t_rh_thread.serial == None:
                self.start_sensor.emit()
                print("serial created")
        else:
            # print("Temperature/RH sensor disconnected.")
            self.set_sensor_status.emit("temp_rh", "Disconnected", "red")

            # close serial port if not already closed
            if self.t_rh_thread.serial != None:
                self.stop_sensor.emit()

                print("serial stopped")

    def check_phidget(self):
        if self.phidget_thread.is_attached == False:
            # ~ print("Light sensor disconnected. Trying to connect...")
            self.set_sensor_status.emit("light", "Disconnected", "red")

            try:
                self.phidget_thread.light_sensor.openWaitForAttachment(1000)
            except:
                print("Unable to connect light sensor...")
        else:
            # ~ print("Light sensor connected.")
            self.set_sensor_status.emit("light", "Connected", "green")

    def check_wind(self):
        wind_direction_cardinal = self.weather_thread.sensors.degrees_to_cardinal(
            self.weather_thread.sensors.wind_direction
        )

        if self.weather_thread.sensors.updated_wind_rain:
            print("wind sensors updated")
            self.wind_speed = self.weather_thread.sensors.wind_speed
            self.wind_dir = wind_direction_cardinal

    @pyqtSlot(str, float)
    def set_wind(self, direction, speed):
        self.wind_speed = speed
        self.wind_speed_history.append(self.wind_speed)
        self.wind_dir = direction

        # send values out
        dispatcher.send(
            signal="broadcast_wind",
            sender={"wind_speed": self.wind_speed, "wind_dir": self.wind_dir},
        )

    def getAverageSpeed(self):
        average = statistics.fmean(self.wind_speed_history)
        self.wind_speed_history = []
        return average

    def clearAverages(self):
        self.wind_speed_history = []

    def run(self):
        while True:
            # ~ print("Checking for sensors...")
            self.check_temp_humidity()
            self.check_phidget()
            # ~ self.check_wind()
            time.sleep(5)
