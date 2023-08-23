import yaml
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from widgets.settings_view.slider_manager.temp_slider import TempSlider
from widgets.settings_view.slider_manager.hum_slider import HumSlider

from helpers import resource_path


class SliderManager(QWidget):
    def __init__(self):
        super(SliderManager, self).__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_widgets()

    def setup_widgets(self):
        try:
            path = resource_path("settings.yml")
            self.config = yaml.safe_load(open(path))
        except:
            print("Error reading settings.yml")

        self.temp_slider = TempSlider(self.config["temperature_offset"])
        self.hum_slider = HumSlider(self.config["humidity_offset"])

        self.layout.addWidget(self.temp_slider)
        self.layout.addWidget(self.hum_slider)
