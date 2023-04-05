from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPalette, QColor

from widgets.main_view.live_tabs import LiveTabs
from widgets.main_view.options import Options

class ContentBox(QWidget):
  def __init__(self, timelapse_thread):
    super(ContentBox, self).__init__()
    
    layout = QHBoxLayout()
    self.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)

    layout.addWidget(LiveTabs(), 2)
    layout.addWidget(Options(timelapse_thread), 1)
