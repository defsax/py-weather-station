from pydispatch import dispatcher

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox, QDialog
from helpers import delete_files


class Dialog(QDialog):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.setWindowTitle("Notice!")

        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        message = QLabel(f"Are you sure you want to {command} all data?")

        self.layout = QVBoxLayout()
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        self.done(0)
        print("yes")
        if self.command == "output":
            print("outputting to usb...")
            # send output signal out
            dispatcher.send(
                signal="output_files_signal",
                sender="output",
            )

        else:
            print("deleting all data...")
            delete_files("/home/pi/weather_station_data/*")

    def reject(self):
        print("no")
        self.done(0)
