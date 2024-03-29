import yaml
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QAbstractItemView,
    QLabel,
)
from widgets.settings_view.id_manager.buttons import ButtonsWidget

from helpers import resource_path
from constants import BASIC_FONT_SIZE, BLUE


class IdManager(QWidget):
    def __init__(self):
        super(IdManager, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 10, 10)
        self.setLayout(layout)

        self.mission_id_label = QLabel("Mission IDs:")
        font = self.mission_id_label.font()
        font.setPointSize(BASIC_FONT_SIZE)
        self.mission_id_label.setFont(font)

        self.add_id_label = QLabel("Add new mission ID:")
        font = self.add_id_label.font()
        font.setPointSize(BASIC_FONT_SIZE)
        self.add_id_label.setFont(font)

        self.id_area = QListWidget()
        self.id_area.setSelectionMode(QAbstractItemView.SingleSelection)
        font = self.id_area.font()
        font.setPointSize(BASIC_FONT_SIZE)
        self.id_area.setFont(font)

        self.id_area.setStyleSheet("selection-background-color: " + BLUE)

        self.add_box = QLineEdit()
        self.add_remove_buttons = ButtonsWidget(self)

        try:
            path = resource_path("settings.yml")
            self.config = yaml.safe_load(open(path))
        except:
            print("Error reading settings.yml")

        # for i, item in enumerate(self.config["mission_ids"]):
        for item in self.config["mission_ids"]:
            self.id_area.addItem(item)

        layout.addWidget(self.mission_id_label)
        layout.addWidget(self.id_area)
        layout.addWidget(self.add_id_label)
        layout.addWidget(self.add_box)
        layout.addWidget(self.add_remove_buttons)
