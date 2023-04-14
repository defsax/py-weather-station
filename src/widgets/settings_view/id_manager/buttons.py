from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class ButtonsWidget(QWidget):
    def __init__(self, parent):
        super(ButtonsWidget, self).__init__()

        self.id_manager = parent
        self.id_manager.id_area.currentItemChanged.connect(self.on_selection_change)
        self.id_manager.add_box.textChanged.connect(self.on_textbox_change)

        self.selected_item = None

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.add_button = QPushButton()
        self.add_button.setText("Add")
        self.add_button.clicked.connect(self.add_item)
        self.add_button.setEnabled(False)

        self.remove_button = QPushButton()
        self.remove_button.setText("Remove")
        self.remove_button.clicked.connect(self.remove_item)
        self.remove_button.setEnabled(False)

        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)

    def add_item(self):
        print("adding item:", self.id_manager.add_box.text())
        mission_id = self.id_manager.add_box.text()
        self.id_manager.id_area.addItem(mission_id)
        self.id_manager.add_box.clear()
        self.add_button.setEnabled(False)

    def remove_item(self):
        row = self.id_manager.id_area.row(self.selected_item)
        self.id_manager.id_area.takeItem(row)

        # self.remove_button.setEnabled(False)

    def on_selection_change(self, current):
        self.selected_item = current
        if self.selected_item:
            self.remove_button.setEnabled(True)
        else:
            self.remove_button.setEnabled(False)

    def on_textbox_change(self, value):
        if value:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)
