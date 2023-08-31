import os
import sys

from pyudev.pyqt5 import MonitorObserver
from pyudev import Context, Monitor
from distutils.dir_util import copy_tree
from pydispatch import dispatcher

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

from widgets.title_bar.title_bar import TitleBar
from widgets.main_view.main_view import MainView
from widgets.settings_view.settings_view import SettingsView
from widgets.hat_display.display_thread import DisplayThread

from dispatcher.senders import update_file_status, update_usb_status

from threads.timelapse_thread import TimelapseThread
from threads.server import ServerThread
from threads.sensor_manager import SensorManager

from helpers import copy_single
from constants import PATH_DATA_FOLDER


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
        self.setup_dispatchers()
        self.setup_usb()

    def __del__(self):
        print("\nApp unwind.")

    #
    # Setup specific functions
    #

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
        self.overall_layout.setContentsMargins(0, 0, 0, 0)
        self.overall_layout.setSpacing(0)

        # dummy widget to hold layout, layout holds actual widgets
        widget = QWidget()
        widget.setLayout(self.overall_layout)

        # dummy widget used as central widget
        self.setCentralWidget(widget)

    def setup_widgets(self):
        self.main_view = MainView()
        self.settings_view = SettingsView()
        self.title = TitleBar(self.main_view, self.settings_view)

    def setup_dispatchers(self):
        dispatcher.connect(
            self.toggle_timelapse, signal="toggle_logging", sender=dispatcher.Any
        )
        dispatcher.connect(
            self.handle_shutdown, signal="shutdown_signal", sender=dispatcher.Any
        )
        dispatcher.connect(
            self.copy_files, signal="output_files_signal", sender=dispatcher.Any
        )

    # USB Monitor Setup
    def setup_usb(self):
        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by(subsystem="block", device_type="partition")
        self.observer = MonitorObserver(monitor)
        self.observer.deviceEvent.connect(self.device_connected)

        monitor.start()

        # super hacky please change
        try:
            if os.path.exists("/media/pi/" + next(os.walk("/media/pi"))[1][0]):
                print("usb already inserted")
                self.device_connected(type("", (object,), {"action": "change"})())
        except:
            print("cannot open usb")

    def device_connected(self, device):
        print(device.action)
        # get mountpoint folder
        directory = next(os.walk("/media/pi"))[1]

        # wait until "change", so that device is mounted
        if device.action == "change" and directory:
            new_path = os.path.join("/media/pi", directory[0])
            self.usb_path = new_path
            update_usb_status(True)
        if device.action == "remove":
            print("No device or device removed.")
            update_usb_status(False)

    #
    # Key bindings and related functions
    #

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

    #
    # Dispatcher specific functions
    #

    def toggle_timelapse(self, sender):
        mission_id = self.main_view.content.options.drop_down.combobox.currentText()
        if not mission_id:
            print("no mission id!")
            return

        if sender["msg"] == "start":
            self.main_view.content.options.start_stop_button.set_button_style(
                "Stop", "red"
            )
            self.timelapse_thread.setup(mission_id)
            self.timelapse_thread.start()
        elif sender["msg"] == "stop":
            self.main_view.content.options.start_stop_button.set_button_style(
                "Start", "green"
            )
            self.timelapse_thread.stop()

    def handle_shutdown(self, sender):
        print(sender, "shutdown!!!")
        os.system("systemctl poweroff")

    def copy_files(self, sender):
        new_path = self.usb_path + "/weather_station_data/"
        if not os.path.exists(new_path):
            update_file_status(
                self.usb_path + "/weather_station_data/ does not exist. Creating..."
            )
            print(self.usb_path + "/weather_station_data/ does not exist. Creating...")
            os.makedirs(new_path)

        print("sender", sender)
        if sender["cmd"] == "all":
            # copy all
            update_file_status("Exporting all files...")
            copy_tree(PATH_DATA_FOLDER, new_path)
            update_file_status("Done exporting.")
        if sender["cmd"] == "single":
            # copy one
            file_name = sender["file_name"]
            update_file_status(f"Exporting {file_name}...")
            file_path = os.path.join(PATH_DATA_FOLDER, file_name)
            print(file_path)
            copy_single(file_path, new_path)
            update_file_status(f"Done exporting {file_name}.")

        print("DONE")


app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
