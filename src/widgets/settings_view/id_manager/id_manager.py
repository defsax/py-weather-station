import yaml
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QAbstractItemView,
    QListWidgetItem,
    QLabel,
)
from widgets.settings_view.id_manager.buttons import ButtonsWidget


class IdManager(QWidget):
    def __init__(self):
        super(IdManager, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        self.mission_id_label = QLabel("Mission IDs:")
        font = self.mission_id_label.font()
        font.setPointSize(14)
        self.mission_id_label.setFont(font)

        self.add_id_label = QLabel("Add new mission ID:")
        font = self.mission_id_label.font()
        font.setPointSize(14)
        self.mission_id_label.setFont(font)

        self.add_remove_buttons = ButtonsWidget(self)

        self.add_box = QLineEdit()

        self.id_area = QListWidget()
        self.id_area.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.id_area.connect.itemClicked(self.item_)

        self.id_area.currentItemChanged.connect(self.on_selection_changed)

        self.config = yaml.safe_load(
            open("/home/pi/code/python/py-weather-station/settings.yml")
        )
        for i, item in enumerate(self.config["mission_ids"]):
            # ~ print(item)
            self.id_area.addItem(item)

        for i in range(100):
            item = QListWidgetItem("Item %i" % i)
            self.id_area.addItem(item)

        layout.addWidget(self.mission_id_label)
        layout.addWidget(self.id_area)
        layout.addWidget(self.add_id_label)
        layout.addWidget(self.add_box)
        layout.addWidget(self.add_remove_buttons)

    def on_selection_changed(self, current, previous):
        print("selected", current, previous)
        if not self.id_area.selectedItems():
            # Do Stuff Here
            print("nothing selected")
            # self.nothing_selected_function()
        # else:
