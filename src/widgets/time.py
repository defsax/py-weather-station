from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

from threads.clock_thread import ClockThread

class Time(QWidget):
  def __init__(self):
    super(Time, self).__init__()

    layout = QHBoxLayout()
    self.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)

    # time display
    self.time = QLabel("")
    font = self.time.font()
    font.setPointSize(14)
    self.time.setFont(font)

    self.clock = ClockThread()
    self.clock.set_time.connect(self.set_time)
    self.clock.start()

    layout.addWidget(self.time)
    
    print("time init")

  @pyqtSlot(str)      
  def set_time(self, time_str):
    self.time.setText(time_str)
