import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QComboBox
from PyQt5.QtGui import QPalette, QColor

from pydispatch import dispatcher

class StatusBox(QWidget):

  def __init__(self, default_msg):
    super(StatusBox, self).__init__()
    
    layout = QVBoxLayout()
    
    self.status = QLabel("Waiting...")
    font = self.status.font()
    font.setPointSize(16)
    self.status.setFont(font)
    self.status.setStyleSheet("QLabel { color : orange; }")
    
