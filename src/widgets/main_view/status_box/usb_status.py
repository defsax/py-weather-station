from pydispatch import dispatcher
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout


class USBStatus(QWidget):
    def __init__(self):
        super(USBStatus, self).__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("USB drive... ")
        # font = title.font()
        # font.setPointSize(16)

        self.status = QLabel("Disconnected")
        # font = self.status.font()
        # font.setPointSize(16)
        self.status.setStyleSheet("color: red")

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status)

        self.is_inserted = False

        dispatcher.connect(
            self.set_status, signal="usb_is_inserted", sender=dispatcher.Any
        )

    def set_status(self, sender):
        self.is_inserted = sender

        if sender:
            text_color = "green"
            status = "Connected"
        else:
            text_color = "red"
            status = "Disconnected"

        format_string = '<font color="{0}">{1}</font>'
        self.status.setText(format_string.format(text_color, status))
