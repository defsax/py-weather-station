from PyQt5.QtWidgets import QWidget, QVBoxLayout

from widgets.main_view.live_tabs import LiveTabs
from widgets.main_view.options import Options


class ContentBox(QWidget):
    def __init__(self):
        super(ContentBox, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.live_tabs = LiveTabs()
        self.options = Options()

        layout.addWidget(self.live_tabs, 2)
        layout.addWidget(self.options, 1)
