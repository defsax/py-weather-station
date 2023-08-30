from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

from widgets.title_bar.settings_button import SettingsButton
from widgets.title_bar.time import Time


class TitleBar(QWidget):
    def __init__(self, main, settings):
        super(TitleBar, self).__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.setStyleSheet(
            "border-bottom: 1px solid grey; border-right: none; border-left: none; margin: 0px"
        )
        # self.setStyleSheet("padding: 10px; border-radius: 10px; background-color: red")
        # layout.setFont(QtGui.QFont("AnyStyle", 16))

        # context dependent label
        self.title = QLabel("Weather Station")
        font = self.title.font()
        font.setPointSize(18)
        self.title.setFont(font)
        self.title.setStyleSheet("padding: 0px; margin: 0px; border-radius: 0px;")

        # time and time thread
        time = Time()

        settings_button = SettingsButton(main, settings)

        layout.addWidget(self.title, 1)
        # layout.addStretch()
        layout.addWidget(time, 1)
        layout.addWidget(settings_button)
        layout.setAlignment(Qt.AlignTop)
