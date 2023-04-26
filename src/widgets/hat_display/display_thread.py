from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal

import time
import ST7789
from PIL import Image
from widgets.hat_display.sensor_data import SensorData
from widgets.hat_display.config import Config
from widgets.hat_display.view_controller import ViewController
from widgets.hat_display.views import *


class DisplayThread(QThread):
    def __init__(self, sensor_manager):
        super(DisplayThread, self).__init__()

        self.sensor_manager = sensor_manager

        self.DISPLAY_WIDTH = 240
        self.DISPLAY_HEIGHT = 240
        self.SPI_SPEED_MHZ = 80
        self.FPS = 10

        self.display = ST7789.ST7789(
            rotation=0,
            port=0,
            cs=1,
            dc=9,
            backlight=13,
            spi_speed_hz=self.SPI_SPEED_MHZ * 1000 * 1000,
        )
        self.image = Image.new(
            "RGBA",
            (self.DISPLAY_WIDTH * 2, self.DISPLAY_HEIGHT * 2),
            color=(255, 255, 255),
        )
        self.sensordata = SensorData(sensor_manager)
        settings = Config()
        self.viewcontroller = ViewController(
            (
                MainView(self.image, self.sensordata, settings),
                (
                    # ~ MainView(image, sensordata, settings),
                    # ~ MainViewGraph(image, sensordata, settings)
                ),
                (
                    # ~ WindDirectionView(image, sensordata, settings),
                    # ~ WindSpeedView(image, sensordata, settings)
                ),
                # ~ RainView(image, sensordata, settings),
                # ~ LightView(image, sensordata, settings),
                (
                    # ~ TemperatureView(image, sensordata, settings),
                    # ~ PressureView(image, sensordata, settings),
                    # ~ HumidityView(image, sensordata, settings)
                ),
            )
        )
        self.start()

    def run(self):
        while True:
            self.sensordata.update(interval=5.0)
            self.viewcontroller.update()
            self.viewcontroller.render()
            self.display.display(
                self.image.resize((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)).convert(
                    "RGB"
                )
            )
            time.sleep(1.0 / self.FPS)
