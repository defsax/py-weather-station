import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSlider
)
# ~ from widgets.content_container import ContentBox

class SettingsView(QMainWindow):
    def __init__(self):
      super(SettingsView, self).__init__()
    
      # ~ self.setup_widgets(timelapse_thread)
      self.setup_ui()
      
    def setup_ui(self):      
      # create layout containers
      self.overall_layout = QVBoxLayout()
      # ~ self.overall_layout.addWidget(self.content)  
    
      self.overall_layout.setContentsMargins(0, 0, 0, 0)
    
      self.slider = QSlider(Qt.Orientation.Horizontal, self)
      self.slider.setRange(-1, 1)
      self.slider.setSingleStep(0.25)
      self.overall_layout.addWidget(self.slider)
    
 
      layout = QHBoxLayout()
      # ~ self.setLayout(layout)
      layout.setContentsMargins(0, 0, 0, 0)

      # ~ layout.addWidget(LiveTabs(), 2)
      # ~ layout.addWidget(Options(timelapse_thread), 1)
    
 
      
      # dummy widget to hold layout, layout holds actual widgets
      widget = QWidget()
      widget.setLayout(self.overall_layout)

      # dummy widget used as central widget
      self.setCentralWidget(widget)
      
    
    # ~ def setup_widgets(self, timelapse_thread):
      # ~ self.content = ContentBox(timelapse_thread)
