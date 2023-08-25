from os import listdir
from os.path import isfile, join
from pydispatch import dispatcher


from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QAbstractItemView,
)

from widgets.settings_view.data_manager.delete_buttons import DeleteButtons
from widgets.settings_view.data_manager.output_buttons import OutputDataButtons
from widgets.main_view.status_box.usb_status import USBStatus

from helpers import delete_files
from constants import PATH_DATA_FOLDER, BASIC_FONT_SIZE


class DataManager(QWidget):
    def __init__(self):
        super(DataManager, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.usb_status = USBStatus()
        self.selected_item = None

        self.data_area = QListWidget()
        font = self.data_area.font()
        font.setPointSize(BASIC_FONT_SIZE)
        self.data_area.setFont(font)

        self.data_area.setSelectionMode(QAbstractItemView.SingleSelection)
        self.data_area.currentItemChanged.connect(self.on_selection_change)

        self.output_buttons = OutputDataButtons()
        self.delete_buttons = DeleteButtons(self.remove_item)

        self.refresh_data_list()

        layout.addWidget(self.data_area)
        layout.addWidget(self.usb_status)
        layout.addWidget(self.output_buttons)
        layout.addWidget(self.delete_buttons)

        dispatcher.connect(
            self.on_usb_change,
            signal="usb_is_inserted",
            sender=dispatcher.Any,
        )
        dispatcher.connect(
            self.refresh_data_list,
            signal="refresh_file_data",
            sender=dispatcher.Any,
        )

    def on_selection_change(self, current):
        self.selected_item = current
        print("on_selection_change", self.selected_item)

        if self.selected_item and self.usb_status.is_inserted:
            self.output_buttons.export_single_button.setEnabled(True)
        else:
            self.output_buttons.export_single_button.setEnabled(False)

        if self.selected_item:
            self.delete_buttons.delete_item_button.setEnabled(True)
        else:
            self.delete_buttons.delete_item_button.setEnabled(False)

    def remove_item(self):
        # row = self.data_area.row(self.selected_item)
        # print(self.selected_item.text())
        # self.data_area.takeItem(row)

        delete_files(PATH_DATA_FOLDER + self.selected_item.text())
        self.refresh_data_list()

    def on_usb_change(self, sender):
        # is_enabled is whether usb is inserted or not
        is_enabled = sender

        print(len(self.get_list_items()))

        # if there are items in the list and the usb is inserted:
        if len(self.get_list_items()) and is_enabled:
            self.output_buttons.export_all_button.setEnabled(is_enabled)

        # if there is an item selected and the usb is inserted:
        if self.selected_item and is_enabled:
            self.output_buttons.export_single_button.setEnabled(is_enabled)

        # if the usb is removed:
        if not is_enabled:
            self.output_buttons.export_single_button.setEnabled(is_enabled)
            self.output_buttons.export_all_button.setEnabled(is_enabled)

    def refresh_data_list(self):
        self.data_area.clear()

        # path = "/home/pi/weather_station_data"

        try:
            onlyfiles = [
                f
                for f in listdir(PATH_DATA_FOLDER)
                if isfile(join(PATH_DATA_FOLDER, f))
            ]
        except:
            print("Error reading settings.yml")

        if len(onlyfiles):
            self.delete_buttons.delete_all_button.setEnabled(True)
            for file in onlyfiles:
                self.data_area.addItem(file)

        else:
            self.delete_buttons.delete_all_button.setEnabled(False)

    def get_list_items(self):
        items = [self.data_area.item(x) for x in range(self.data_area.count())]
        return items
