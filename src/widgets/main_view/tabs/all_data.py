from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from pydispatch import dispatcher


class DataDisplay(QWidget):
    def __init__(self):
        super(DataDisplay, self).__init__()

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        status = QLabel("00")
        font = status.font()
        font.setPointSize(75)
        status.setFont(font)
        status.setAlignment(Qt.AlignCenter)

        status_wind_speed = QLabel("01")
        font = status_wind_speed.font()
        font.setPointSize(75)
        status_wind_speed.setFont(font)
        status_wind_speed.setAlignment(Qt.AlignCenter)

        status_wind_dir = QLabel("10")
        font = status_wind_dir.font()
        font.setPointSize(75)
        status_wind_dir.setFont(font)
        status_wind_dir.setAlignment(Qt.AlignCenter)

        status_light = QLabel("11")
        font = status_light.font()
        font.setPointSize(75)
        status_light.setFont(font)
        status_light.setAlignment(Qt.AlignCenter)

        self.status_temperature = QLabel("20")
        font = self.status_temperature.font()
        font.setPointSize(75)
        self.status_temperature.setFont(font)
        self.status_temperature.setAlignment(Qt.AlignCenter)

        self.status_humidity = QLabel("21")
        font = self.status_humidity.font()
        font.setPointSize(75)
        self.status_humidity.setFont(font)
        self.status_humidity.setAlignment(Qt.AlignCenter)

        grid_layout.addWidget(status, 0, 0)
        grid_layout.addWidget(status_wind_speed, 0, 1)
        grid_layout.addWidget(status_wind_dir, 1, 0)
        grid_layout.addWidget(status_light, 1, 1)
        grid_layout.addWidget(self.status_temperature, 2, 0)
        grid_layout.addWidget(self.status_humidity, 2, 1)

        dispatcher.connect(
            self.update_values, signal="broadcast_serial", sender=dispatcher.Any
        )

    def update_values(self, sender):
        self.status_humidity = ""
        self.status_temperature = ""
