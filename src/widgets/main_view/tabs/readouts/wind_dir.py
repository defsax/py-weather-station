from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from pydispatch import dispatcher


class WindDirDisplay(QWidget):
    def __init__(self):
        super(WindDirDisplay, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.status_direction = QLabel("")
        font = self.status_direction.font()
        font.setPointSize(75)
        self.status_direction.setFont(font)
        self.status_direction.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.label = QLabel("direction  ")
        font = self.label.font()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignRight)

        layout.addWidget(self.status_direction)
        layout.addWidget(self.label)

        dispatcher.connect(
            self.update_values, signal="broadcast_wind", sender=dispatcher.Any
        )

    def update_values(self, sender):
        wd = [s[0] for s in sender["wind_dir"].split()]
        d = "".join(wd)
        self.status_direction.setText(d)
