from pydispatch import dispatcher
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

class LightStatus(QWidget):
  def __init__(self):
    super(LightStatus, self).__init__()
    
    layout = QHBoxLayout()
    self.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Light sensor... ")
    font = title.font()
    font.setPointSize(16)
    
    self.status = QLabel("Connected")
    font = self.status.font()
    font.setPointSize(16)
    
    layout.addWidget(title)
    layout.addStretch()
    layout.addWidget(self.status)
    
    dispatcher.connect(self.set_status, signal = "set_light_status", sender = dispatcher.Any)
    
  def set_status(self, sender):
    text_color = sender["col"]
    status = sender["status"]
    format_string = '<font color="{0}">{1}</font>'
    self.status.setText(format_string.format(text_color, status))
