import os

from distutils.dir_util import copy_tree
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

from pyudev.pyqt5 import MonitorObserver
from pyudev import Context, Monitor


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
        dispatcher.connect(
            self.copy_files, signal="output_files_signal", sender=dispatcher.Any
        )

        #####
        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by(subsystem="block", device_type="partition")
        self.observer = MonitorObserver(monitor)
        self.observer.deviceEvent.connect(self.device_connected)
        monitor.start()

    def device_connected(self, device):
        # self.textBrowser.append(device.sys_name)
        # print("Test")
        # print("device node", device.device_node)
        # print("device type", device.device_type)
        # p = self.find_mount_point(device.device_node)
        # print(p)
        # print("device path", device.device_path)
        # print("device sys_name", device.sys_name)
        # print("device sys_path", device.sys_path)

        # print(next(os.walk("/media/pi"))[1])
        dirs = next(os.walk("/media/pi"))[1]
        if dirs:
            print(dirs)
            new_path = os.path.join("/media/pi", dirs[0])
            print(new_path)
            self.usb_path = new_path

        # for root, dirs, files in os.walk("/media/pi"):
        #     print("root", root)
        #     print("dirs", dirs)
        #     print("files", files)
        # print(root, "consumes")
        # print(sum(os.path.getsize(os.path.join(root, name)) for name in files))
        # print("bytes in", len(files), "non-directory files")

    # def find_mount_point(self, path):
    #     path = os.path.abspath(path)
    #     while not os.path.ismount(path):
    #         path = os.path.dirname(path)
    #     return path

    ######

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

    def copy_files(self):
        new_path = self.usb_path + "/weather_station_data/"
        if not os.path.exists(new_path):
            print(self.usb_path + "/weather_station_data/ does not exist. Creating...")
            os.makedirs(new_path)

        copy_tree("/home/pi/weather_station_data/", new_path)
        print("DONE")
        # 2nd option
        # shutil.copy2(
        #     "/home/pi/weather_station_data/", self.usb_path
        #     )  # dst can be a folder; use shutil.copy2() to preserve timestamp

    def handle_shutdown(self, sender):
        print(sender, "shutdown!!!")
        os.system("systemctl poweroff")


app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
