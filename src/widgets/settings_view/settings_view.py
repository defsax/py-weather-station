import yaml
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from widgets.settings_view.temp_slider import TempSlider
from widgets.settings_view.hum_slider import HumSlider
from widgets.settings_view.id_manager.id_manager import IdManager
from widgets.settings_view.shutdown_button import ShutdownButton


class SettingsView(QMainWindow):
    def __init__(self):
        super(SettingsView, self).__init__()

        self.setup_widgets()
        self.setup_ui()

    def setup_ui(self):
        # create layout containers
        self.overall_layout = QVBoxLayout()

        self.overall_layout.setContentsMargins(0, 0, 0, 0)
        self.overall_layout.addWidget(self.temp_slider)
        self.overall_layout.addWidget(self.hum_slider)
        self.overall_layout.addWidget(self.id_manager)
        self.overall_layout.addWidget(self.shutdown_button)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # dummy widget to hold layout, layout holds actual widgets
        widget = QWidget()
        widget.setLayout(self.overall_layout)

        # dummy widget used as central widget
        self.setCentralWidget(widget)

    def setup_widgets(self):
        try:
            self.config = yaml.safe_load(
                open("/home/pi/code/python/py-weather-station/settings.yml")
            )
        except:
            print("Error reading settings.yml")

        self.temp_slider = TempSlider(self.config["temperature_offset"])
        self.hum_slider = HumSlider(self.config["humidity_offset"])
        self.id_manager = IdManager()
        self.shutdown_button = ShutdownButton()
