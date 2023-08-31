from pydispatch import dispatcher


def update_file_status(message):
    dispatcher.send(
        signal="update_file_transfer_status",
        sender=message,
    )


def export_all_files():
    dispatcher.send(
        signal="output_files_signal",
        sender={"cmd": "all"},
    )


def export_single_file(item_name):
    dispatcher.send(
        signal="output_files_signal",
        sender={"cmd": "single", "file_name": item_name},
    )
