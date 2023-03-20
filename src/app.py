import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    QMenuBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from widgets.title_bar import TitleBar
from widgets.content_container import ContentBox

class MainWindow(QMainWindow):
    def __init__(self):
      super(MainWindow, self).__init__()

      #start full screen
      # ~ self.showFullScreen()
      
      # ~ self.setFixedWidth(800)
      # ~ self.setFixedHeight(480)
      self.setGeometry(100, 100, 800, 480)
      
      # ~ widget = QLabel("Welcome to the Weather Station")
      # ~ font = widget.font()
      # ~ font.setPointSize(30)
      # ~ widget.setFont(font)
      # ~ widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

      # ~ self.setCentralWidget(widget)
      self.setup_widgets()
      self.setup_ui()
      
    def __del__(self):
      print("\nApp unwind.")
      
    def setup_ui(self):      
      # create layout containers
      self.overall_layout = QVBoxLayout()
      self.overall_layout.addWidget(self.title)  
      self.overall_layout.addWidget(self.content)  
      
      self.overall_layout.setContentsMargins(10, 10, 10, 10)
      
      # dummy widget to hold layout, layout holds actual widgets
      widget = QWidget()
      widget.setLayout(self.overall_layout)

      # dummy widget used as central widget
      self.setCentralWidget(widget)
      
    
    def setup_widgets(self):
      self.title = TitleBar()
      self.content = ContentBox()

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
