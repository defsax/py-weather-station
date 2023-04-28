from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from pydispatch import dispatcher


class HumidityDisplay(QWidget):
    def __init__(self):
        super(HumidityDisplay, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.status_humidity = QLabel("")
        font = self.status_humidity.font()
        font.setPointSize(75)
        self.status_humidity.setFont(font)
        self.status_humidity.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.label = QLabel("%rh")
        font = self.label.font()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignRight)

        layout.addWidget(self.status_humidity)
        layout.addWidget(self.label)

        dispatcher.connect(
            self.update_values, signal="broadcast_serial", sender=dispatcher.Any
        )

    def update_values(self, sender):
        rh = round(sender["current_humidity"] + sender["offset_h"], 1)

        if rh > 99:
            self.status_humidity.setText("N/A")
        else:
            self.status_humidity.setText(str(rh))
