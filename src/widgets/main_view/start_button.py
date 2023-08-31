from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from dispatcher.senders import toggle_data_logging


class StartStop(QWidget):
    def __init__(self):
        super(StartStop, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.start_btn = QPushButton("Start", self)
        self.start_btn.clicked.connect(self.handle_start)
        self.start_btn.setStyleSheet(
            "padding: 10px; border-radius: 0px; background-color: green"
        )
        self.start_btn.setFont(QtGui.QFont("AnyStyle", 25))

        layout.addWidget(self.start_btn)

    def handle_start(self):
        if self.start_btn is not None:
            text = self.start_btn.text()
            if text == "Start":
                toggle_data_logging("start")
            else:
                toggle_data_logging("stop")

    def set_button_style(self, msg, col):
        if self.start_btn is not None:
            self.start_btn.setText(msg)
            self.start_btn.setStyleSheet(
                "padding: 10px; border-radius: 0px; background-color: " + col
            )
