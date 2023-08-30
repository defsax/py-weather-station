import yaml

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget

from widgets.settings_view.id_manager.id_manager import IdManager
from widgets.settings_view.data_manager.data_manager import DataManager
from widgets.settings_view.slider_manager.slider_manager import SliderManager
from widgets.settings_view.shutdown_button import ShutdownButton

from helpers import resource_path, load_stylesheet
from constants import BASIC_FONT_SIZE, PATH_TABS_STYLESHEET


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
        self.tabs.setStyleSheet(load_stylesheet(PATH_TABS_STYLESHEET, "tabs_style.qss"))

        self.tabs.setDocumentMode(True)

        font = self.tabs.font()
        font.setPointSize(BASIC_FONT_SIZE)
        self.tabs.setFont(font)

        self.overall_layout.addWidget(self.tabs)
        self.overall_layout.addStretch()
        self.overall_layout.addWidget(self.shutdown_button)

        self.overall_layout.setContentsMargins(0, 0, 0, 0)
        self.overall_layout.setSpacing(10)

        self.tabs.addTab(self.slider_manager, "Calibration")
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

        self.id_manager = IdManager()
        self.data_manager = DataManager()
        self.slider_manager = SliderManager()
        self.shutdown_button = ShutdownButton()
