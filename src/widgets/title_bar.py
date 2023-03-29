from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor

from widgets.settings_button import SettingsButton
from widgets.time import Time

class TitleBar(QWidget):

  def __init__(self, parent):
    super(TitleBar, self).__init__()

    layout = QHBoxLayout()
    self.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)

    # context dependent label
    title = QLabel("Weather Station")
    font = title.font()
    font.setPointSize(16)
    title.setFont(font)
    
    # time and time thread
    time = Time()
    
    settings_button = SettingsButton(parent)

    layout.addWidget(title)
    layout.addStretch()
    layout.addWidget(time)
    layout.addWidget(settings_button)
    layout.setAlignment(Qt.AlignTop)
