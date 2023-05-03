from pydispatch import dispatcher

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox, QDialog


class ShutdownDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure you want to shut down?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        self.done(0)
        print("yes")
        # send shutdown signal out
        dispatcher.send(
            signal="shutdown_signal",
            sender="shutdown",
        )

    def reject(self):
        print("no")
        self.done(0)
