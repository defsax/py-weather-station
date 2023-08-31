from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from pydispatch import dispatcher

from helpers import write_to_yaml, resource_path
from constants import PATH_SETTINGS_ICON
from dispatcher.senders import refresh_data_box, update_temp_rh_offset


class SettingsButton(QWidget):
    def __init__(self, main_view, settings_view):
        super(SettingsButton, self).__init__()

        self.main_view = main_view
        self.settings_view = settings_view

        self.button = QPushButton("", self)
        self.button.clicked.connect(self.handleButton)
        self.button.setIconSize(QSize(45, 45))
        # self.button.setIconSize(QSize(25, 25))
        self.button.setStyleSheet(
            "border-left: 1px solid grey; padding: 10px; margin: 0px; border-radius: 0px"
        )

        try:
            path = PATH_SETTINGS_ICON
            self.button.setIcon(QIcon(path))

        except:
            path = resource_path("settings-icon.png")
            self.button.setIcon(QIcon(path))

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.button)
        self.setLayout(layout)

        dispatcher.connect(
            self.toggle_status, signal="toggle_logging", sender=dispatcher.Any
        )

    def handleButton(self):
        if self.main_view.isVisible():
            refresh_data_box()

            # switch views
            self.main_view.hide()
            self.settings_view.show()
        else:
            id_area = self.settings_view.id_manager.id_area
            mission_ids = [id_area.item(x).text() for x in range(id_area.count())]
            self.main_view.content.options.drop_down.load_mission_ids(mission_ids)

            # save settings to yaml
            write_to_yaml(
                "humidity_offset", self.settings_view.slider_manager.hum_slider.offset
            )
            write_to_yaml(
                "temperature_offset",
                self.settings_view.slider_manager.temp_slider.offset,
            )
            write_to_yaml("mission_ids", mission_ids)

            # update arduino handler with the correct slider values
            h_offset = self.settings_view.slider_manager.hum_slider.offset
            t_offset = self.settings_view.slider_manager.temp_slider.offset
            update_temp_rh_offset(h_offset, t_offset)

            # switch views
            self.main_view.show()
            self.settings_view.hide()

    def toggle_status(self, sender):
        if sender["msg"] == "start":
            self.button.setEnabled(False)
        elif sender["msg"] == "stop":
            self.button.setEnabled(True)
