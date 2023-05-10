from PyQt5.QtCore import Qt, QFile, QIODevice, QTextStream
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel

from pydispatch import dispatcher
from helpers import resource_path


class HumSlider(QWidget):
    def __init__(self, offset):
        super(HumSlider, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(layout)

        self.offset = offset
        print(self.offset, type(self.offset))
        self.current_humidity = 0

        self.label = QLabel("Humidity Offset: " + str(self.offset))
        font = self.label.font()
        font.setPointSize(14)
        self.label.setFont(font)

        self.rh_reference = QLabel(str(self.current_humidity + offset))
        font = self.rh_reference.font()
        font.setPointSize(14)
        self.rh_reference.setFont(font)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(-40, 40)
        self.slider.setValue(int(self.offset * 4))
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.valueChanged.connect(self.update)

        # load style for slider
        try:
            path = "/home/pi/code/python/py-weather-station/src/widgets/settings_view/slider_style.qss"
            print("literal path")
        except:
            path = resource_path("slider_style.qss")
            print("resource path")

        try:
            stream = QFile(path)
            stream.open(QIODevice.ReadOnly)
            self.slider.setStyleSheet(QTextStream(stream).readAll())
        except:
            print("issue loading qss")

        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        widget.setLayout(horizontal_layout)
        horizontal_layout.addWidget(self.label)
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.rh_reference)

        layout.addWidget(widget)
        layout.addWidget(self.slider)

        # receive rh from sensor
        dispatcher.connect(
            self.get_values, signal="broadcast_serial", sender=dispatcher.Any
        )

    def get_values(self, sender):
        self.current_humidity = sender["current_humidity"]

        format_string = "<font>{0}% rh</font>"
        self.rh_reference.setText(
            format_string.format(str(self.current_humidity + self.offset))
        )

    def update(self, value):
        self.offset = float(value) / 4
        format_string = "<font>Humidity Offset: {0}</font>"
        self.label.setText(format_string.format(self.offset))

        format_string = "<font>{0}% rh</font>"
        self.rh_reference.setText(
            format_string.format(str(self.current_humidity + self.offset))
        )
