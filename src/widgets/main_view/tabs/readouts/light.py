from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from pydispatch import dispatcher


class LightDisplay(QWidget):
    def __init__(self):
        super(LightDisplay, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.status_light = QLabel("")
        font = self.status_light.font()
        font.setPointSize(75)
        self.status_light.setFont(font)
        self.status_light.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.label = QLabel("wm2  ")
        font = self.label.font()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignRight)

        layout.addWidget(self.status_light)
        layout.addWidget(self.label)

        dispatcher.connect(
            self.update_values, signal="broadcast_light", sender=dispatcher.Any
        )

    def update_values(self, sender):
        l = str(round(sender["wm2"]))
        # l = str(round(sender["wm2"], 1))
        self.status_light.setText(l)
