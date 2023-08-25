from pydispatch import dispatcher

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from widgets.settings_view.data_manager.dialog import Dialog

from helpers import delete_files
from constants import PATH_DATA_FOLDER


class DeleteButtons(QWidget):
    def __init__(self, remove_item):
        super(DeleteButtons, self).__init__()

        self.item = ""
        self.remove_item = remove_item

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.delete_item_button = QPushButton()
        self.delete_item_button.setText("Delete Item")
        self.delete_item_button.clicked.connect(
            lambda: self.double_check(
                self.delete_item, f"Are you sure you want to delete {self.item}?"
            )
        )
        self.delete_item_button.setEnabled(False)

        self.delete_all_button = QPushButton()
        self.delete_all_button.setText("Delete All Data")
        self.delete_all_button.clicked.connect(
            lambda: self.double_check(
                self.delete_all, "Are you sure you want to delete all data?"
            )
        )
        self.delete_all_button.setEnabled(True)

        layout.addWidget(self.delete_item_button)
        layout.addWidget(self.delete_all_button)

    def double_check(self, export_method, prompt):
        print("Delete data button...")
        dlg = Dialog(export_method, prompt)
        dlg.setWindowTitle("Alert!")
        dlg.exec()

    def delete_all(self):
        print("deleting all data...")

        # Add * to delete all
        delete_files(PATH_DATA_FOLDER + "*")

        dispatcher.send(
            signal="refresh_file_data",
            sender="output",
        )

    def delete_item(self):
        print(f"deleting{self.item}...")
        self.remove_item()
