import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    QMenuBar,
    QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
      super(MainWindow, self).__init__()

      #start full screen
      # ~ self.showFullScreen()
      
      self.setFixedWidth(800)
      self.setFixedHeight(480)
      
      widget = QLabel("Welcome to the Weather Station")
      font = widget.font()
      font.setPointSize(30)
      widget.setFont(font)
      widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

      self.setCentralWidget(widget)
      
    def __del__(self):
      print("\nApp unwind.")
      

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
          self.close()
        if e.key() == Qt.Key_F11:
          self.toggleFullScreen()

    def toggleFullScreen(self):
      if self.isFullScreen():
        self.showNormal()
      else:
        self.showFullScreen()

app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
