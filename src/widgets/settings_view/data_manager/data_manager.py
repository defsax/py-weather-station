from os import listdir
from os.path import isfile, join

from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QAbstractItemView,
)

from widgets.settings_view.data_manager.delete_button import DeleteButton
from widgets.settings_view.data_manager.output_button import OutputDataButton


class DataManager(QWidget):
    def __init__(self):
        super(DataManager, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.id_area = QListWidget()
        self.id_area.setSelectionMode(QAbstractItemView.SingleSelection)

        path = "/home/pi/weather_station_data"

        try:
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            # path = resource_path("settings.yml")
            # self.config = yaml.safe_load(open(path))
        except:
            print("Error reading settings.yml")

        for file in onlyfiles:
            print(file)
            self.id_area.addItem(file)

        # delete all / delete single
        # export all / export single

        self.output_button = OutputDataButton()
        self.delete_button = DeleteButton()

        layout.addWidget(self.id_area)
        layout.addWidget(self.output_button)
        layout.addWidget(self.delete_button)
