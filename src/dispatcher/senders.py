from pydispatch import dispatcher


def update_file_status(message):
    dispatcher.send(
        signal="update_file_transfer_status",
        sender=message,
    )
