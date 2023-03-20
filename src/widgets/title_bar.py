import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QHBoxLayout, QStyle
from PyQt5.QtGui import QPalette, QColor

from widgets.settings_button import SettingsButton

class TitleBar(QWidget):

  def __init__(self):
    super(TitleBar, self).__init__()
    
    layout = QHBoxLayout()
    self.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Weather Station")
    font = title.font()
    font.setPointSize(16)
    title.setFont(font)
    
    settings_button = SettingsButton()
    
    layout.addWidget(title)
    layout.addStretch()
    layout.addWidget(settings_button)
    layout.setAlignment(Qt.AlignTop)
