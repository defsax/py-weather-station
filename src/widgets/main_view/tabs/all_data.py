from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout

from widgets.main_view.tabs.readouts.hum import HumidityDisplay
from widgets.main_view.tabs.readouts.temp import TemperatureDisplay
from widgets.main_view.tabs.readouts.light import LightDisplay
from widgets.main_view.tabs.readouts.voltage import VoltageDisplay
from widgets.main_view.tabs.readouts.wind_speed import WindSpeedDisplay
from widgets.main_view.tabs.readouts.wind_dir import WindDirDisplay


class DataDisplay(QWidget):
    def __init__(self):
        super(DataDisplay, self).__init__()

        # layout = QVBoxLayout()
        # self.setLayout(layout)
        # layout.setContentsMargins(0, 0, 0, 0)

        # row_one = QHBoxLayout()
        # row_one.addWidget(VoltageDisplay())
        # row_one.addWidget(LightDisplay())
        # row_one_widget = QWidget()
        # row_one_widget.setLayout(row_one)

        # row_two = QHBoxLayout()
        # row_two.addWidget(WindSpeedDisplay())
        # row_two.addWidget(WindDirDisplay())
        # row_two_widget = QWidget()
        # row_two_widget.setLayout(row_two)

        # row_three = QHBoxLayout()
        # row_three.addWidget(TemperatureDisplay())
        # row_three.addWidget(HumidityDisplay())
        # row_three_widget = QWidget()
        # row_three_widget.setLayout(row_three)

        # layout.addWidget(row_one_widget)
        # layout.addWidget(row_two_widget)
        # layout.addWidget(row_three_widget)

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        grid_layout.addWidget(VoltageDisplay(), 0, 0)
        grid_layout.addWidget(LightDisplay(), 0, 1)

        grid_layout.addWidget(WindSpeedDisplay(), 1, 0)
        grid_layout.addWidget(WindDirDisplay(), 1, 1)
        grid_layout.addWidget(TemperatureDisplay(), 2, 0)
        grid_layout.addWidget(HumidityDisplay(), 2, 1)

        grid_layout.setSpacing(2)
        grid_layout.setHorizontalSpacing(0)
