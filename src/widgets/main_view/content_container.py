from PyQt5.QtWidgets import QWidget, QVBoxLayout

from widgets.main_view.options import Options
from widgets.main_view.tabs.all_data import DataDisplay


class ContentBox(QWidget):
    def __init__(self):
        super(ContentBox, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.options = Options()

        layout.addWidget(DataDisplay(), 2)
        layout.addWidget(self.options, 1)
