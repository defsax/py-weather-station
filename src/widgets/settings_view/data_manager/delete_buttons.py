from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from widgets.settings_view.data_manager.dialog import Dialog


class DeleteButtons(QWidget):
    def __init__(self, remove_item):
        super(DeleteButtons, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.delete_item_button = QPushButton()
        self.delete_item_button.setText("Delete Item")
        self.delete_item_button.clicked.connect(remove_item)
        self.delete_item_button.setEnabled(False)

        self.delete_all_button = QPushButton()
        self.delete_all_button.setText("Delete All Data")
        self.delete_all_button.clicked.connect(self.double_check)
        self.delete_all_button.setEnabled(True)

        # self.delete_all_button.setStyleSheet(
        #     "padding: 10px; border-radius: 10px; background-color: rgba(255, 0, 0, 0.3)"
        # )
        # self.delete_all_button.setFont(QtGui.QFont("AnyStyle", 16))
        layout.addWidget(self.delete_item_button)
        layout.addWidget(self.delete_all_button)

    def double_check(self):
        print("Delete data button...")
        dlg = Dialog("delete")
        dlg.setWindowTitle("Alert!")
        dlg.exec()
