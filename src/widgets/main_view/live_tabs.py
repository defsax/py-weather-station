from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QVBoxLayout,
)


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

    # ~ def add_cams_to_tabs(self, cameras):
    # ~ for i, cam in enumerate(cameras):
    # ~ self.tabs.addTab(cam, self.check_icon, "Camera {}".format(i+1))
