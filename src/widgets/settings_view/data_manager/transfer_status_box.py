from pydispatch import dispatcher

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

from threads.message_queue_thread import MessageQueueThread
from constants import BASIC_FONT_SIZE


class FileTranferStatusBox(QWidget):
    def __init__(self):
        super(FileTranferStatusBox, self).__init__()

        self.msg_queue = MessageQueueThread()
        self.msg_queue.output_message.connect(self.set_status)

        dispatcher.connect(
            self.queue_message, signal="update_file_status", sender=dispatcher.Any
        )

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Status... ")
        # font = title.font()
        # font.setPointSize(BASIC_FONT_SIZE)
        # title.setFont(font)

        self.status = QLabel("Ready")
        # font = self.status.font()
        # font.setPointSize(BASIC_FONT_SIZE)
        # self.status.setFont(font)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status)

    def queue_message(self, sender):
        self.msg_queue.add_message(sender["message"], sender["duration"])

    @pyqtSlot(str)
    def set_status(self, message):
        self.status.setText(message)
