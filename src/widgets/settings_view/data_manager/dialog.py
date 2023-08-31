# from pydispatch import dispatcher

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox, QDialog

# from helpers import delete_files
# from constants import PATH_DATA_FOLDER


class Dialog(QDialog):
    def __init__(self, callback, command):
        super().__init__()
        self.callback = callback
        self.command = command
        self.setWindowTitle("Notice!")

        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        message = QLabel(self.command)

        self.layout = QVBoxLayout()
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        self.done(0)
        print("yes")
        self.callback()

    def reject(self):
        print("no")
        self.done(0)
