from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from widgets.settings_view.data_manager.dialog import Dialog
from dispatcher.senders import refresh_data_box, update_file_status

from helpers import delete_files
from constants import PATH_DATA_FOLDER, RED


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

        self.set_style()

    def double_check(self, export_method, prompt):
        print("Delete data button...")
        dlg = Dialog(export_method, prompt)
        dlg.setWindowTitle("Alert!")
        dlg.exec()

    def delete_all(self):
        try:
            update_file_status("Deleting all data...")

            # Add * to delete all
            delete_files(PATH_DATA_FOLDER + "*")
        except:
            update_file_status("Error deleting all data.", 4)
        else:
            update_file_status("Deleted all data.", 4)
        finally:
            update_file_status("Ready")
            refresh_data_box()

    def delete_item(self):
        print(f"deleting{self.item}...")
        self.remove_item()

    def set_style(self):
        self.delete_all_button.setStyleSheet(
            "QPushButton{ padding: 10px; border-radius: 0px; } :enabled { background-color: "
            + RED
            + "; color: #000; } :disabled { background-color: #cccccc; color: #666666;}"
        )
        self.delete_item_button.setStyleSheet(
            "QPushButton{ padding: 10px; border-radius: 0px; } :enabled { background-color: "
            + RED
            + "; color: #000; } :disabled { background-color: #cccccc; color: #666666;}"
        )
        self.delete_all_button.setFont(QtGui.QFont("AnyStyle", 20))
        self.delete_item_button.setFont(QtGui.QFont("AnyStyle", 20))
