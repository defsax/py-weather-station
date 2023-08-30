from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from widgets.settings_view.shutdown_dialog import ShutdownDialog


class ShutdownButton(QWidget):
    def __init__(self):
        super(ShutdownButton, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.shutdown_btn = QPushButton("Shutdown", self)
        self.shutdown_btn.clicked.connect(self.handle_shutdown)

        self.shutdown_btn.setStyleSheet(
            "padding: 10px; border-radius: 0px; background-color: red"
        )
        self.shutdown_btn.setFont(QtGui.QFont("AnyStyle", 16))
        layout.addWidget(self.shutdown_btn)

    def handle_shutdown(self):
        print("shutdown")
        dlg = ShutdownDialog()
        dlg.setWindowTitle("Alert!")
        dlg.exec()
