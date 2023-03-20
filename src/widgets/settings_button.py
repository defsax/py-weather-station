from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStyle, QGridLayout


class SettingsButton(QWidget):
  def __init__(self):
    super(SettingsButton, self).__init__()
    
    pixmapi = getattr(QStyle, 'SP_FileIcon')
    icon = self.style().standardIcon(pixmapi)
    
    self.button = QPushButton('', self)
    self.button.clicked.connect(self.handleButton)
    # ~ self.button.setIconSize(QtCore.QSize(20,20))
    self.button.setIcon(icon)
    print('button init')
    
    layout = QHBoxLayout()
    layout.addWidget(self.button)
    self.setLayout(layout)

  def handleButton(self):
    print("settings button")  
