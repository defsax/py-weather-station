from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QVBoxLayout,
)

from widgets.main_view.tabs.all_data import DataDisplay


class LiveTabs(QWidget):
    def __init__(self):
        super(LiveTabs, self).__init__()

        self.layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        # ~ tabs.setIconSize(QSize(20,20))
        self.tabs.setMovable(True)

        # set layout and style
        self.layout.addWidget(self.tabs)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.tabs.addTab(DataDisplay(), "Data")
