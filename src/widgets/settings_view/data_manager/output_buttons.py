from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from widgets.settings_view.data_manager.dialog import Dialog
from dispatcher.senders import export_all_files, export_single_file


class OutputDataButtons(QWidget):
    def __init__(self):
        super(OutputDataButtons, self).__init__()

        self.item = ""

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.export_single_button = QPushButton()
        self.export_single_button.setText("Export Item")
        self.export_single_button.clicked.connect(
            lambda: self.double_check(
                lambda: export_single_file(self.item),
                f"Are you sure you want to export {self.item}?",
            )
        )
        self.export_single_button.setEnabled(False)

        self.export_all_button = QPushButton()
        self.export_all_button.setText("Export All Data")
        self.export_all_button.clicked.connect(
            lambda: self.double_check(
                export_all_files, "Are you sure you want to export all data?"
            )
        )
        self.export_all_button.setEnabled(False)

        layout.addWidget(self.export_single_button)
        layout.addWidget(self.export_all_button)

    def double_check(self, export_method, prompt):
        print("Output data button...")
        dlg = Dialog(export_method, prompt)
        dlg.setWindowTitle("Alert!")
        dlg.exec()
