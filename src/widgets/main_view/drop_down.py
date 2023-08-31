import yaml
from pydispatch import dispatcher
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox

from helpers import resource_path


class DropDown(QWidget):
    def __init__(self):
        super(DropDown, self).__init__()

        self.combobox = QComboBox()
        self.load_mission_ids()

        layout = QHBoxLayout()
        layout.addWidget(self.combobox)
        self.setLayout(layout)

        dispatcher.connect(
            self.toggle_status, signal="toggle_logging", sender=dispatcher.Any
        )

    def handleButton(self):
        print("settings button")

    def load_mission_ids(self, list=None):
        if list == None:
            try:
                path = resource_path("settings.yml")
                self.config = yaml.safe_load(open(path))
            except:
                print("Error loading settings for mission ids.")
            for item in self.config["mission_ids"]:
                self.combobox.addItem(item)
        else:
            # clear self.combobox
            self.combobox.clear()

            # add new list
            for item in list:
                self.combobox.addItem(item)

    def toggle_status(self, sender):
        if sender["msg"] == "start":
            self.combobox.setEnabled(False)
        elif sender["msg"] == "stop":
            self.combobox.setEnabled(True)
