from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout

from widgets.main_view.start_button import StartQuit
from widgets.main_view.drop_down import DropDown

class Options(QWidget):
  def __init__(self, timelapse_thread):
    super(Options, self).__init__()
    
    layout = QVBoxLayout()
    self.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Enter Mission ID")
    font = title.font()
    font.setPointSize(16)
    title.setFont(font)
    title.setAlignment(Qt.AlignCenter)
    
    
    layout.addStretch()
    layout.addWidget(title)
    layout.addWidget(DropDown())
    layout.addStretch()
    layout.addWidget(StartQuit(timelapse_thread))

    layout.setAlignment(Qt.AlignTop)
