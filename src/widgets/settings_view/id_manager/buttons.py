from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class ButtonsWidget(QWidget):
    def __init__(self, parent):
        super(ButtonsWidget, self).__init__()

        self.id_manager = parent

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        add_button = QPushButton()
        add_button.setText("Add")
        add_button.clicked.connect(self.add_item)

        remove_button = QPushButton()
        remove_button.setText("Remove")
        remove_button.clicked.connect(self.remove_item)

        layout.addWidget(add_button)
        layout.addWidget(remove_button)

    def add_item(self):
        print("add item")

    def remove_item(self):
        print("remove item")
