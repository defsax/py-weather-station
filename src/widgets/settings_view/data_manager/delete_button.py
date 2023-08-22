from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from widgets.settings_view.data_manager.dialog import Dialog


class DeleteButton(QWidget):
    def __init__(self):
        super(DeleteButton, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.delete_button = QPushButton()
        self.delete_button.setText("Delete Data")
        self.delete_button.clicked.connect(self.double_check)
        self.delete_button.setEnabled(True)

        self.delete_button.setStyleSheet(
            "padding: 10px; border-radius: 10px; background-color: rgba(255, 0, 0, 0.3)"
        )
        self.delete_button.setFont(QtGui.QFont("AnyStyle", 16))
        layout.addWidget(self.delete_button)

    def double_check(self):
        print("Delete data button...")
        dlg = Dialog("delete")
        dlg.setWindowTitle("Alert!")
        dlg.exec()
