import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout

from widgets.start_button import StartQuit

class Options(QWidget):

  def __init__(self):
    super(Options, self).__init__()
    
    layout = QVBoxLayout()
    self.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Options")
    font = title.font()
    font.setPointSize(16)
    title.setFont(font)
    title.setAlignment(Qt.AlignCenter)
    
    
    layout.addWidget(title)
    layout.addStretch()
    layout.addWidget(StartQuit())

    layout.setAlignment(Qt.AlignTop)
