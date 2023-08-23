import yaml

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget

from widgets.settings_view.temp_slider import TempSlider
from widgets.settings_view.hum_slider import HumSlider
from widgets.settings_view.id_manager.id_manager import IdManager
from widgets.settings_view.data_manager.data_manager import DataManager
from widgets.settings_view.shutdown_button import ShutdownButton

from helpers import resource_path


class SettingsView(QMainWindow):
    def __init__(self):
        super(SettingsView, self).__init__()

        self.setup_widgets()
        self.setup_ui()

    def setup_ui(self):
        # create layout containers
        self.overall_layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setIconSize(QSize(20, 20))
        self.tabs.setMovable(True)

        self.overall_layout.addWidget(self.tabs)
        self.overall_layout.setContentsMargins(0, 0, 0, 0)
        self.overall_layout.setSpacing(10)

        # self.overall_layout.addWidget(self.temp_slider)
        # self.overall_layout.addWidget(self.hum_slider)
        self.overall_layout.addWidget(self.shutdown_button)

        self.tabs.addTab(self.id_manager, "IDs")
        self.tabs.addTab(self.data_manager, "Data")

        # dummy widget to hold layout, layout holds actual widgets
        widget = QWidget()
        widget.setLayout(self.overall_layout)

        # dummy widget used as central widget
        self.setCentralWidget(widget)

    def setup_widgets(self):
        try:
            path = resource_path("settings.yml")
            self.config = yaml.safe_load(open(path))
        except:
            print("Error reading settings.yml")

        self.temp_slider = TempSlider(self.config["temperature_offset"])
        self.hum_slider = HumSlider(self.config["humidity_offset"])
        self.id_manager = IdManager()
        self.data_manager = DataManager()
        self.shutdown_button = ShutdownButton()
