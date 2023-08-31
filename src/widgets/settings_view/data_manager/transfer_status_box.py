from pydispatch import dispatcher

from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout


class FileTranferStatusBox(QWidget):
    def __init__(self):
        super(FileTranferStatusBox, self).__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Status... ")
        # font = title.font()
        # font.setPointSize(16)

        self.status = QLabel("")
        # font = self.status.font()
        # font.setPointSize(16)
        self.status.setStyleSheet("color: grey")

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status)

        self.is_inserted = False

        dispatcher.connect(
            self.set_status, signal="update_file_transfer_status", sender=dispatcher.Any
        )

    def set_status(self, sender):
        # self.is_inserted = sender

        text_color = "grey"
        status = sender

        # if sender:
        #     text_color = "green"
        #     status = "Connected"
        # else:
        #     text_color = "red"
        #     status = "Disconnected"
        # format_string = '<font color="{0}">{1}</font>'

        self.status.setText(f'<font color="{text_color}">{status}</font>')
