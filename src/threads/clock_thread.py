import time
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal


class ClockThread(QThread):
    # set up pyqtsignal
    set_time = pyqtSignal(str)

    def __init__(self):
        super(ClockThread, self).__init__()

    def run(self):
        while True:
            formatted_time = datetime.now().strftime("%a, %b %d %H:%M:%S")
            self.set_time.emit(formatted_time)
            time.sleep(1)
