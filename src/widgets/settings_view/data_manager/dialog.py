# from pydispatch import dispatcher

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

        self.layout = QVBoxLayout()

        # s1, s2, s3 = 'Python', 'String', 'Concatenation'
        # s = f'{s1} {s2} {s3}'
        # if command == "output":
        message = QLabel(f"Are you sure you want to {command} all data?")
        # else:
        #     message = QLabel("Are you sure you want to shut down?")

        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        self.done(0)
        print("yes")
        if self.command == "output":
            print("outputting to usb...")
        else:
            print("deleting all data...")
            delete_files("/home/pi/weather_station_data/*")

        # send shutdown signal out
        # dispatcher.send(
        #     signal="shutdown_signal",
        #     sender="shutdown",
        # )

    def reject(self):
        print("no")
        self.done(0)
