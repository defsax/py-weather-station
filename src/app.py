import os
import sys
from pydispatch import dispatcher

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from widgets.title_bar.title_bar import TitleBar
from widgets.main_view.main_view import MainView
from widgets.settings_view.settings_view import SettingsView
from widgets.hat_display.display_thread import DisplayThread

from threads.timelapse_thread import TimelapseThread
from threads.server import ServerThread
from threads.sensor_manager import SensorManager


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # ~ self.setFixedWidth(800)
        # ~ self.setFixedHeight(480)
        # self.setGeometry(100, 100, 480, 800)
        self.setFixedSize(480, 800)

        # start full screen
        self.showFullScreen()

        self.setup_threads()
        self.setup_widgets()
        self.setup_ui()

        dispatcher.connect(
            self.toggle_timelapse, signal="toggle_logging", sender=dispatcher.Any
        )
        dispatcher.connect(
            self.handle_shutdown, signal="shutdown_signal", sender=dispatcher.Any
        )

    def __del__(self):
        print("\nApp unwind.")

    def setup_threads(self):
        self.sensor_manager = SensorManager()
        self.timelapse_thread = TimelapseThread(self.sensor_manager)
        self.display_thread = DisplayThread(self.sensor_manager)
        self.server_thread = ServerThread()

    def setup_ui(self):
        # create layout containers
        self.overall_layout = QVBoxLayout()
        self.overall_layout.addWidget(self.title)
        self.overall_layout.addWidget(self.main_view)
        self.overall_layout.addWidget(self.settings_view)
        self.main_view.show()
        self.settings_view.hide()
        self.overall_layout.setContentsMargins(10, 10, 10, 10)

        # dummy widget to hold layout, layout holds actual widgets
        widget = QWidget()
        widget.setLayout(self.overall_layout)

        # dummy widget used as central widget
        self.setCentralWidget(widget)

    def toggle_timelapse(self, sender):
        mission_id = self.main_view.content.options.drop_down.combobox.currentText()
        if not mission_id:
            print("no mission id!")
            return

        if sender["msg"] == "start":
            dispatcher.send(signal="logging_status", sender={"msg": "start"})
            self.main_view.content.options.start_stop_button.set_button_style(
                "Stop", "red"
            )
            self.timelapse_thread.setup(mission_id)
            self.timelapse_thread.start()
        elif sender["msg"] == "stop":
            dispatcher.send(signal="logging_status", sender={"msg": "stop"})
            self.main_view.content.options.start_stop_button.set_button_style(
                "Start", "green"
            )
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

    def handle_shutdown(self, sender):
        print(sender, "shutdown!!!")
        os.system("systemctl poweroff")


app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
