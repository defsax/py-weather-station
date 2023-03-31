import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QSizePolicy

class StartQuit(QWidget):
  def __init__(self, timelapse_thread):
    super(StartQuit, self).__init__()
    
    self.timelapse_thread = timelapse_thread
    
    layout = QVBoxLayout()
    layout.setContentsMargins(5, 0, 0, 0)
    self.setLayout(layout)
    
    self.start_btn = QPushButton("Start", self)
    self.start_btn.clicked.connect(self.handle_start)
    
    # ~ self.start_btn.setSizePolicy(
        # ~ QSizePolicy.Preferred,
        # ~ QSizePolicy.Expanding)
    # ~ self.start_btn.setGeometry(200, 150, 100, 40)
    self.start_btn.setStyleSheet("padding: 10px; border-radius: 10px; background-color: green")
    self.start_btn.setFont(QtGui.QFont('AnyStyle', 25))
    layout.addWidget(self.start_btn)
    
    # start with start button disabled
    # ~ self.start_btn.setEnabled(False)

    
  def handle_start(self):
    if self.start_btn is not None:
      text = self.start_btn.text()
      if text == "Start":
        print("start")
        self.start_btn.setText("Stop")
        self.start_btn.setStyleSheet("padding: 10px; border-radius: 10px; background-color: red")
        self.timelapse_thread.setup()
        self.timelapse_thread.start()
      else:
        print("stop")
        self.timelapse_thread.stop()
        self.start_btn.setText("Start")
        self.start_btn.setStyleSheet("padding: 10px; border-radius: 10px; background-color: green")
