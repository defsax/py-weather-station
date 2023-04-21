from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from pydispatch import dispatcher


class WindSpeedDisplay(QWidget):
    def __init__(self):
        super(WindSpeedDisplay, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.status_speed = QLabel("")
        font = self.status_speed.font()
        font.setPointSize(75)
        self.status_speed.setFont(font)
        self.status_speed.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.label = QLabel("m/s")
        font = self.label.font()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignRight)

        layout.addWidget(self.status_speed)
        layout.addWidget(self.label)

        dispatcher.connect(
            self.update_values, signal="broadcast_wind", sender=dispatcher.Any
        )

    def update_values(self, sender):
        w = str(round(sender["wind_speed"], 1))
        self.status_speed.setText(w)
