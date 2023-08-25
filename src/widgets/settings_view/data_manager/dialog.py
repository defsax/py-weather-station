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

        # if self.command == "output":
        #     print("outputting to usb...")
        #     # send output signal out
        #     dispatcher.send(
        #         signal="output_files_signal",
        #         sender="output",
        #     )

        # else:
        #     print("deleting all data...")
        #     # Add * to delete all
        #     delete_files(PATH_DATA_FOLDER + "*")
        #     # delete_files("/home/pi/weather_station_data/*")
        #     dispatcher.send(
        #         signal="refresh_file_data",
        #         sender="output",
        #     )

    def reject(self):
        print("no")
        self.done(0)
