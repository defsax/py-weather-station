from pydispatch import dispatcher

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class StartStop(QWidget):
    def __init__(self):
        super(StartStop, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.start_btn = QPushButton("Start", self)
        self.start_btn.clicked.connect(self.handle_start)

        # ~ self.start_btn.setSizePolicy(
        # ~ QSizePolicy.Preferred,
        # ~ QSizePolicy.Expanding)
        # ~ self.start_btn.setGeometry(200, 150, 100, 40)
        self.start_btn.setStyleSheet(
            "padding: 10px; border-radius: 0px; background-color: green"
        )
        self.start_btn.setFont(QtGui.QFont("AnyStyle", 25))
        layout.addWidget(self.start_btn)

    def handle_start(self):
        if self.start_btn is not None:
            text = self.start_btn.text()
            if text == "Start":
                dispatcher.send(signal="toggle_logging", sender={"msg": "start"})

                # self.start_btn.setText("Stop")
                # self.start_btn.setStyleSheet(
                #     "padding: 10px; border-radius: 10px; background-color: red"
                # )
            else:
                dispatcher.send(signal="toggle_logging", sender={"msg": "stop"})

                # self.start_btn.setText("Start")
                # self.start_btn.setStyleSheet(
                #     "padding: 10px; border-radius: 10px; background-color: green"
                # )

    def set_button_style(self, msg, col):
        if self.start_btn is not None:
            self.start_btn.setText(msg)
            self.start_btn.setStyleSheet(
                "padding: 10px; border-radius: 10px; background-color: " + col
            )
