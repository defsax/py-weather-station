from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStyle


class SettingsButton(QWidget):
  def __init__(self, main_view):
    super(SettingsButton, self).__init__()
    
    self.main_view = main_view
    
    pixmapi = getattr(QStyle, 'SP_FileIcon')
    icon = self.style().standardIcon(pixmapi)
    
    self.button = QPushButton('', self)
    self.button.clicked.connect(self.handleButton)
    # ~ self.button.setIconSize(QtCore.QSize(20,20))
    self.button.setIcon(icon)
    
    layout = QHBoxLayout()
    layout.addWidget(self.button)
    self.setLayout(layout)

  def handleButton(self):
    if self.main_view.isVisible():
        print("Settings...")
        self.main_view.hide()
    else:
        print("Main...")
        self.main_view.show()
    # ~ self.hide()
