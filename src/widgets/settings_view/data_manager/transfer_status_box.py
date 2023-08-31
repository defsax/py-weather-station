from pydispatch import dispatcher

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

from threads.message_queue_thread import MessageQueueThread


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
        # font.setPointSize(16)

        self.status = QLabel("Ready")
        # font = self.status.font()
        # font.setPointSize(16)
        self.status.setStyleSheet("color: grey")

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status)

    def queue_message(self, sender):
        self.msg_queue.add_message(sender["message"], sender["duration"])

    @pyqtSlot(str)
    def set_status(self, message):
        # self.is_inserted = sender
        print("status box message:", message)

        text_color = "grey"

        # if sender:
        #     text_color = "green"
        #     status = "Connected"
        # else:
        #     text_color = "red"
        #     status = "Disconnected"
        # format_string = '<font color="{0}">{1}</font>'

        self.status.setText(f'<font color="{text_color}">{message}</font>')
