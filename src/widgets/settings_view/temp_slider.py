from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel

from pydispatch import dispatcher


class TempSlider(QWidget):
    def __init__(self, offset):
        super(TempSlider, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        self.offset = offset
        print(self.offset, type(self.offset))
        self.current_temperature = 0

        self.label = QLabel("Temperature Offset: " + str(self.offset))
        font = self.label.font()
        font.setPointSize(14)
        self.label.setFont(font)

        self.t_reference = QLabel(str(self.current_temperature + offset))
        font = self.t_reference.font()
        font.setPointSize(14)
        self.t_reference.setFont(font)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(-40, 40)
        self.slider.setValue(int(self.offset * 4))
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.valueChanged.connect(self.update)

        horizontal_layout = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(horizontal_layout)
        horizontal_layout.addWidget(self.label)
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.t_reference)

        layout.addWidget(widget)
        layout.addWidget(self.slider)

        # receive temp from sensor
        dispatcher.connect(
            self.get_values, signal="broadcast_serial", sender=dispatcher.Any
        )

    def get_values(self, sender):
        self.current_temperature = sender["current_temperature"]

        format_string = "<font>{0}°C</font>"
        self.t_reference.setText(
            format_string.format(str(self.current_temperature + self.offset))
        )

    def update(self, value):
        self.offset = float(value) / 4
        print(value, self.offset)

        format_string = "<font>Temperature Offset: {0}</font>"
        self.label.setText(format_string.format(self.offset))

        format_string = "<font>{0}°C</font>"
        self.t_reference.setText(
            format_string.format(str(self.current_temperature + self.offset))
        )
