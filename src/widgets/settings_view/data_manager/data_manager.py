from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    # QLineEdit,
    # QListWidget,
    # QAbstractItemView,
    # QLabel,
)

from widgets.settings_view.data_manager.delete_button import DeleteButton
from widgets.settings_view.data_manager.output_button import OutputDataButton


class DataManager(QWidget):
    def __init__(self):
        super(DataManager, self).__init__()

        layout = QHBoxLayout()
        # layout.setContentsMargins(10, 0, 10, 10)
        self.setLayout(layout)

        self.output_button = OutputDataButton()
        self.delete_button = DeleteButton()

        # self.mission_id_label = QLabel("Mission IDs:")
        # font = self.mission_id_label.font()
        # font.setPointSize(14)
        # self.mission_id_label.setFont(font)

        # self.add_id_label = QLabel("Add new mission ID:")
        # font = self.mission_id_label.font()
        # font.setPointSize(14)
        # self.mission_id_label.setFont(font)

        # self.add_box = QLineEdit()

        # self.id_area = QListWidget()
        # self.id_area.setSelectionMode(QAbstractItemView.SingleSelection)

        # self.add_remove_buttons = ButtonsWidget(self)

        layout.addWidget(self.output_button)
        layout.addWidget(self.delete_button)
        # layout.addWidget(self.add_id_label)
        # layout.addWidget(self.add_box)
        # layout.addWidget(self.add_remove_buttons)
