from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from pydispatch import dispatcher


class TemperatureDisplay(QWidget):
    def __init__(self):
        super(TemperatureDisplay, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.status_temperature = QLabel("")
        font = self.status_temperature.font()
        font.setPointSize(75)
        self.status_temperature.setFont(font)
        self.status_temperature.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.label = QLabel("°C")
        font = self.label.font()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignRight)

        layout.addWidget(self.status_temperature)
        layout.addWidget(self.label)

        dispatcher.connect(
            self.update_values, signal="broadcast_serial", sender=dispatcher.Any
        )

    def update_values(self, sender):
        t = str(round(sender["current_temperature"] + sender["offset_t"], 1))
        if t > 99:
            self.status_temperature.setText("N/A")
        else:
            self.status_temperature.setText(t)
