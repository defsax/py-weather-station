from pydispatch import dispatcher

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from widgets.settings_view.data_manager.dialog import Dialog


class OutputDataButton(QWidget):
    def __init__(self):
        super(OutputDataButton, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.output_data_button = QPushButton()
        self.output_data_button.setText("Output Data")
        self.output_data_button.clicked.connect(self.double_check)
        self.output_data_button.setEnabled(False)
        self.output_data_button.setStyleSheet(
            "padding: 10px; border-radius: 10px; background-color: rgba(0, 0, 255, 0.3)"
        )
        self.output_data_button.setFont(QtGui.QFont("AnyStyle", 16))
        layout.addWidget(self.output_data_button)

        dispatcher.connect(
            self.set_enable_output_button,
            signal="enable_output_button",
            sender=dispatcher.Any,
        )

    def double_check(self):
        print("Output data button...")
        dlg = Dialog("output")
        dlg.setWindowTitle("Alert!")
        dlg.exec()

    def set_enable_output_button(self, sender):
        self.output_data_button.setEnabled(sender)
