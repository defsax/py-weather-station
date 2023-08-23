from PyQt5.QtWidgets import QWidget, QHBoxLayout


from widgets.settings_view.data_manager.delete_button import DeleteButton
from widgets.settings_view.data_manager.output_button import OutputDataButton


class DataManager(QWidget):
    def __init__(self):
        super(DataManager, self).__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.output_button = OutputDataButton()
        self.delete_button = DeleteButton()

        layout.addWidget(self.output_button)
        layout.addWidget(self.delete_button)
