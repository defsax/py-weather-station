from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from pydispatch import dispatcher


class VoltageDisplay(QWidget):
    def __init__(self):
        super(VoltageDisplay, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.status_voltage = QLabel("")
        font = self.status_voltage.font()
        font.setPointSize(75)
        self.status_voltage.setFont(font)
        self.status_voltage.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.label = QLabel("V")
        font = self.label.font()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignRight)

        layout.addWidget(self.status_voltage)
        layout.addWidget(self.label)

        dispatcher.connect(
            self.update_values, signal="broadcast_battery", sender=dispatcher.Any
        )

    def update_values(self, sender):
        v = str(round(sender["voltage"], 1))
        self.status_voltage.setText(v)
