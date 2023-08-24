from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from widgets.settings_view.data_manager.dialog import Dialog


class OutputDataButtons(QWidget):
    def __init__(self):
        super(OutputDataButtons, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.export_single_button = QPushButton()
        self.export_single_button.setText("Export Item")
        self.export_single_button.clicked.connect(self.double_check)
        self.export_single_button.setEnabled(False)

        self.export_all_button = QPushButton()
        self.export_all_button.setText("Export All Data")
        self.export_all_button.clicked.connect(self.double_check)
        self.export_all_button.setEnabled(False)
        # self.export_all_button.setStyleSheet(
        #     "padding: 10px; border-radius: 10px; background-color: rgba(0, 0, 255, 0.3)"
        # )
        # self.export_all_button.setFont(QtGui.QFont("AnyStyle", 16))
        layout.addWidget(self.export_single_button)
        layout.addWidget(self.export_all_button)

    def double_check(self):
        print("Output data button...")
        dlg = Dialog("output")
        dlg.setWindowTitle("Alert!")
        dlg.exec()