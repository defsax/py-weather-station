from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPalette, QColor

class ContentBox(QWidget):

  def __init__(self):
    super(ContentBox, self).__init__()
    
    layout = QHBoxLayout()
