import time

from PyQt5.QtCore import QThread, pyqtSignal


class MessageQueueThread(QThread):
    # set up pyqtsignal
    output_message = pyqtSignal(str)

    def __init__(self):
        super(MessageQueueThread, self).__init__()
        self.message_queue = []

    def add_message(self, message, duration):
        self.message_queue.append({"message": message, "duration": duration})
        print("Added message:", message, " time: ", duration)
        if not self.isRunning():
            print("Thread not running... starting...")
            self.start()

    def run(self):
        while self.message_queue:
            self.output_message.emit(self.message_queue[0]["message"])
            time.sleep(self.message_queue[0]["duration"])
            self.message_queue.pop(0)

        print("Thread stopping.")
