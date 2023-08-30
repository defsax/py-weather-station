from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

from threads.clock_thread import ClockThread


class Time(QWidget):
    def __init__(self):
        super(Time, self).__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # time display
        self.time = QLabel("")
        font = self.time.font()
        font.setPointSize(14)
        self.time.setFont(font)

        self.time.setStyleSheet("padding: 0px; margin: 0px; border-radius: 0px; ")

        self.clock = ClockThread()
        self.clock.set_time.connect(self.set_time)
        self.clock.start()

        layout.addWidget(self.time)

    @pyqtSlot(str)
    def set_time(self, time_str):
        self.time.setText(time_str)
