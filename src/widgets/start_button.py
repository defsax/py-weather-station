import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QPushButton


class StartQuit(QWidget):

  def __init__(self):
    super(StartQuit, self).__init__()
    
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(layout)
    
    self.start_btn = QPushButton("Start", self)
    self.start_btn.clicked.connect(self.handle_start)
    layout.addWidget(self.start_btn)
    
    # start with start button disabled
    # ~ self.start_btn.setEnabled(False)
    
    quit_btn = QPushButton("Quit", self)
    # ~ quit_btn.clicked.connect(self.parent.handle_close)
    layout.addWidget(quit_btn)
    

    
  def handle_start(self):
    print("start")
    # ~ if self.start_btn is not None:
      # ~ text = self.start_btn.text()
      # ~ if text == "Start":
        # ~ self.parent.start_timelapse()
        # ~ self.start_btn.setText("Stop")
      # ~ else:
        # ~ self.parent.stop_timelapse()
        # ~ self.start_btn.setText("Start")
