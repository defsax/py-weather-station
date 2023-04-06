from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QComboBox
from PyQt5.QtGui import QPalette, QColor

from widgets.main_view.status_box.temp_rh_status import TempRhStatus
from widgets.main_view.status_box.light_status import LightStatus

class StatusBox(QWidget):

  def __init__(self):
    super(StatusBox, self).__init__()
    
    layout = QVBoxLayout()
    
    self.temp_status = TempRhStatus()
    self.light_status = LightStatus()
        
    layout.addWidget(self.light_status)
    layout.addWidget(self.temp_status)
  
    layout.setAlignment(Qt.AlignBottom)
    self.setLayout(layout)
