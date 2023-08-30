from PyQt5.QtWidgets import QWidget, QGridLayout

from widgets.main_view.tabs.readouts.hum import HumidityDisplay
from widgets.main_view.tabs.readouts.temp import TemperatureDisplay
from widgets.main_view.tabs.readouts.light import LightDisplay
from widgets.main_view.tabs.readouts.voltage import VoltageDisplay
from widgets.main_view.tabs.readouts.wind_speed import WindSpeedDisplay
from widgets.main_view.tabs.readouts.wind_dir import WindDirDisplay


class DataDisplay(QWidget):
    def __init__(self):
        super(DataDisplay, self).__init__()

        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(0)
        # grid_layout.setVerticalSpacing(0)
        # grid_layout.setHorizontalSpacing(0)

        self.setLayout(grid_layout)
        self.setStyleSheet("background-color: white")

        grid_layout.addWidget(VoltageDisplay(), 0, 0)
        grid_layout.addWidget(LightDisplay(), 0, 1)

        grid_layout.addWidget(WindSpeedDisplay(), 1, 0)
        grid_layout.addWidget(WindDirDisplay(), 1, 1)
        grid_layout.addWidget(TemperatureDisplay(), 2, 0)
        grid_layout.addWidget(HumidityDisplay(), 2, 1)
