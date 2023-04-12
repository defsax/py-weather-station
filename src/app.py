import sys
import yaml
from pydispatch import dispatcher

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
from widgets.title_bar.title_bar import TitleBar
from widgets.main_view.main_view import MainView
from widgets.settings_view.settings_view import SettingsView

# ~ from threads.arduino_thread import ArduinoHandler
from threads.timelapse_thread import TimelapseThread
from threads.server import ServerThread

# ~ from helpers import list_serial_devices

class MainWindow(QMainWindow):
    def __init__(self):
      super(MainWindow, self).__init__()

      #start full screen
      # ~ self.showFullScreen()
      
      # ~ self.setFixedWidth(800)
      # ~ self.setFixedHeight(480)
      self.setGeometry(100, 100, 480, 800)
      # ~ self.get_sensors()
      self.setup_threads()
      self.setup_widgets()
      self.setup_ui()
      
      dispatcher.connect(self.toggle_timelapse, signal = "toggle_logging", sender = dispatcher.Any)
      
    def __del__(self):
      print("\nApp unwind.")
      
    # ~ def get_sensors(self):
      # ~ # set up arduinos
      # ~ device_list = list_serial_devices()
      # ~ self.sensors = []
      # ~ if getattr(device_list, 'size', len(device_list)):
        # ~ for device in device_list:
          # ~ print("Arduino connected:", device)
          # ~ self.sensors.append(ArduinoHandler(device))
      # ~ else: 
        # ~ print("No arduino(s) connected")
      
    def setup_threads(self):
      self.timelapse_thread = TimelapseThread()
      self.server_thread = ServerThread()
    
    def setup_ui(self):      
      # create layout containers
      self.overall_layout = QVBoxLayout()
      self.overall_layout.addWidget(self.title) 
      self.overall_layout.addWidget(self.main_view)
      self.overall_layout.setContentsMargins(10, 10, 10, 10)      
      
      # dummy widget to hold layout, layout holds actual widgets
      widget = QWidget()
      widget.setLayout(self.overall_layout)

      # dummy widget used as central widget
      self.setCentralWidget(widget)
    
    def toggle_timelapse(self, sender):
      print("msg",sender["msg"])
      if sender["msg"] == "start":
        self.timelapse_thread.setup()
        self.timelapse_thread.start()
      elif sender["msg"] == "stop":
        self.timelapse_thread.stop()
    
    def setup_widgets(self):
      self.main_view = MainView()
      self.settings_view = SettingsView()
      self.title = TitleBar(self.main_view, self.settings_view)

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
