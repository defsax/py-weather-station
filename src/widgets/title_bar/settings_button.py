from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStyle
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from pydispatch import dispatcher
from helpers import write_to_yaml, resource_path


class SettingsButton(QWidget):
    def __init__(self, main_view, settings_view):
        super(SettingsButton, self).__init__()

        self.main_view = main_view
        self.settings_view = settings_view

        # path = resource_path("settings-icon.png")
        # pixmapi = getattr(QStyle, "SP_FileIcon")
        # icon = self.style().standardIcon(pixmapi)

        self.button = QPushButton("", self)
        self.button.clicked.connect(self.handleButton)
        self.button.setIconSize(QSize(25, 25))
        try:
            path = "/home/pi/code/python/py-weather-station/resources/icons/settings-icon.png"
            self.button.setIcon(QIcon(path))
            print("literal path")
        except:
            path = resource_path("settings-icon.png")
            self.button.setIcon(QIcon(path))
            print("resource path")

        layout = QHBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

        dispatcher.connect(
            self.toggle_status, signal="logging_status", sender=dispatcher.Any
        )

    def handleButton(self):
        if self.main_view.isVisible():
            # if timelapse is running it should stop
            # or, if it's running then disable settings

            # switch views
            self.main_view.hide()
            self.settings_view.show()
        else:
            id_area = self.settings_view.id_manager.id_area
            mission_ids = [id_area.item(x).text() for x in range(id_area.count())]
            self.main_view.content.options.drop_down.load_mission_ids(mission_ids)

            # save settings to yaml
            write_to_yaml("humidity_offset", self.settings_view.hum_slider.offset)
            write_to_yaml("temperature_offset", self.settings_view.temp_slider.offset)
            write_to_yaml("mission_ids", mission_ids)

            # update arduino handler with the correct slider values
            dispatcher.send(
                signal="set_offset",
                sender={
                    "hum_offset": self.settings_view.hum_slider.offset,
                    "temp_offset": self.settings_view.temp_slider.offset,
                },
            )

            # switch views
            self.main_view.show()
            self.settings_view.hide()

    def toggle_status(self, sender):
        if sender["msg"] == "start":
            self.button.setEnabled(False)
        elif sender["msg"] == "stop":
            self.button.setEnabled(True)
