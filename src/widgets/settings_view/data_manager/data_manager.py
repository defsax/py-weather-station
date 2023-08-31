from os import listdir
from os.path import isfile, join
from pydispatch import dispatcher

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QAbstractItemView,
)

from widgets.settings_view.data_manager.delete_buttons import DeleteButtons
from widgets.settings_view.data_manager.output_buttons import OutputDataButtons
from widgets.main_view.status_box.usb_status import USBStatus
from widgets.settings_view.data_manager.transfer_status_box import FileTranferStatusBox

from dispatcher.senders import update_file_status

from helpers import delete_files
from constants import PATH_DATA_FOLDER, BASIC_FONT_SIZE


class DataManager(QWidget):
    def __init__(self):
        super(DataManager, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.file_status = FileTranferStatusBox()
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
        layout.addWidget(self.file_status)
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

        # enable delete item button if selection is made
        if self.selected_item:
            self.delete_buttons.delete_item_button.setEnabled(True)
            self.delete_buttons.item = self.selected_item.text()

        # if there is an item selected and the usb is inserted (updated in two places):
        if self.selected_item and self.usb_status.is_inserted:
            self.output_buttons.export_single_button.setEnabled(True)
            # pass selected item to export item button
            self.output_buttons.item = self.selected_item.text()

        # if there is no selection disable delete and export item buttons
        if not self.selected_item:
            self.output_buttons.export_single_button.setEnabled(False)
            self.delete_buttons.delete_item_button.setEnabled(False)

    def on_usb_change(self, sender):
        # is_enabled is whether usb is inserted or not
        is_usb_inserted = sender

        print(len(self.get_list_items()))

        # if there are items in the list and the usb is inserted:
        if len(self.get_list_items()) and is_usb_inserted:
            self.output_buttons.export_all_button.setEnabled(is_usb_inserted)

        # if there is an item selected and the usb is inserted (updated in two places):
        if self.selected_item and is_usb_inserted:
            self.output_buttons.export_single_button.setEnabled(is_usb_inserted)

        # if the usb is removed:
        if not is_usb_inserted:
            self.output_buttons.export_single_button.setEnabled(is_usb_inserted)
            self.output_buttons.export_all_button.setEnabled(is_usb_inserted)

    def remove_item(self):
        # row = self.data_area.row(self.selected_item)
        # print(self.selected_item.text())
        # self.data_area.takeItem(row)
        update_file_status(f"Deleting {self.selected_item.text()}...")

        delete_files(PATH_DATA_FOLDER + self.selected_item.text())
        self.refresh_data_list()

    def refresh_data_list(self):
        update_file_status("Refreshing file list...")
        self.data_area.clear()

        try:
            onlyfiles = [
                f
                for f in listdir(PATH_DATA_FOLDER)
                if isfile(join(PATH_DATA_FOLDER, f))
            ]
        except:
            print("Error reading settings.yml")

        if len(onlyfiles):
            if self.usb_status.is_inserted:
                self.output_buttons.export_all_button.setEnabled(True)

            self.delete_buttons.delete_all_button.setEnabled(True)
            for file in onlyfiles:
                self.data_area.addItem(file)

        else:
            self.delete_buttons.delete_all_button.setEnabled(False)
            self.output_buttons.export_all_button.setEnabled(False)

        update_file_status("Done refreshing file list...")

    def get_list_items(self):
        items = [self.data_area.item(x) for x in range(self.data_area.count())]
        return items
