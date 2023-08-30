from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout

from widgets.main_view.start_button import StartStop
from widgets.main_view.drop_down import DropDown
from widgets.main_view.status_box.status import StatusBox


class Options(QWidget):
    def __init__(self):
        super(Options, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("Enter Mission ID")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("border-top: 1px solid grey")

        self.drop_down = DropDown()
        self.start_stop_button = StartStop()

        layout.addWidget(title)
        layout.addWidget(self.drop_down)
        layout.addWidget(StatusBox())
        layout.addWidget(self.start_stop_button)

        layout.setAlignment(Qt.AlignTop)
