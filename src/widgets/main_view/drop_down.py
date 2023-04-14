import yaml
from pydispatch import dispatcher
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox


class DropDown(QWidget):
    def __init__(self):
        super(DropDown, self).__init__()

        self.combobox = QComboBox()
        self.load_mission_ids()

        # Connect signals to the methods.
        self.combobox.activated.connect(self.activated)
        self.combobox.currentTextChanged.connect(self.text_changed)
        self.combobox.currentIndexChanged.connect(self.index_changed)

        layout = QHBoxLayout()
        layout.addWidget(self.combobox)
        self.setLayout(layout)

        dispatcher.connect(
            self.toggle_status, signal="logging_status", sender=dispatcher.Any
        )

    def handleButton(self):
        print("settings button")

    def activated(Self, index):
        print("Activated index:", index)

    def text_changed(self, s):
        print("Text changed:", s)

    def index_changed(self, index):
        print("Index changed", index)

    def load_mission_ids(self, list=None):
        if list == None:
            self.config = yaml.safe_load(
                open("/home/pi/code/python/py-weather-station/settings.yml")
            )
            for i, item in enumerate(self.config["mission_ids"]):
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
