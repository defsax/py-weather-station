
import sys

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout
)
from widgets.content_container import ContentBox

class MainView(QMainWindow):
    def __init__(self, timelapse_thread):
      super(MainView, self).__init__()
    
      self.setup_widgets(timelapse_thread)
      self.setup_ui()
      
    def setup_ui(self):      
      # create layout containers
      self.overall_layout = QVBoxLayout()
      self.overall_layout.addWidget(self.content)  
      
      self.overall_layout.setContentsMargins(0, 0, 0, 0)
      
      # dummy widget to hold layout, layout holds actual widgets
      widget = QWidget()
      widget.setLayout(self.overall_layout)

      # dummy widget used as central widget
      self.setCentralWidget(widget)
      
    
    def setup_widgets(self, timelapse_thread):
      self.content = ContentBox(timelapse_thread)
