import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    QMenuBar
)

class MainWindow(QMainWindow):
    def __init__(self):
      super(MainWindow, self).__init__()
      self.setFullscreen = QAction("&Fullscreen", self)
      self.setFullscreen.setShortcut("F11")
      self.setFullscreen.setStatusTip("Change to fullscreen mode")
      self.setFullscreen.triggered.connect(self.toggleFullScreen)
      
      # ~ self.menu = QMenuBar(self)

      # ~ self.file_menu = self.menu.addMenu("&File")
      # ~ self.file_menu.addAction(self.openFile)
      # ~ self.file_menu.addAction(self.saveFile)
      # ~ self.file_menu.addAction(self.exitApp)

      # ~ self.view_menu = self.menu.addMenu("&View")
      # ~ self.view_menu.addAction(self.setFullscreen)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
          self.close()
        if e.key() == Qt.Key_F11:
          self.toggleFullScreen()

    def __del__(self):
      print("\nApp unwind.")

    def toggleFullScreen(self):
      if self.isFullScreen():
        self.showNormal()
      else:
        self.showFullScreen()

app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
