from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStyle

from pydispatch import dispatcher
from helpers import write_to_yaml


class SettingsButton(QWidget):
    def __init__(self, main_view, settings_view):
        super(SettingsButton, self).__init__()

        self.main_view = main_view
        self.settings_view = settings_view

        pixmapi = getattr(QStyle, "SP_FileIcon")
        icon = self.style().standardIcon(pixmapi)

        self.button = QPushButton("", self)
        self.button.clicked.connect(self.handleButton)
        # ~ self.button.setIconSize(QtCore.QSize(20,20))
        self.button.setIcon(icon)

        layout = QHBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def handleButton(self):
        if self.main_view.isVisible():
            print("Settings...")
            self.main_view.hide()
            self.settings_view.show()
        else:
            print("Main...")

            # save slider values
            write_to_yaml("humidity_offset", self.settings_view.hum_slider.offset)
            write_to_yaml("temperature_offset", self.settings_view.temp_slider.offset)

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
