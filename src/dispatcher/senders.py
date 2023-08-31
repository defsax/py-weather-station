from pydispatch import dispatcher


def update_file_status(message):
    dispatcher.send(
        signal="update_file_transfer_status",
        sender=message,
    )


def update_light(light_value):
    dispatcher.send(
        signal="broadcast_light",
        sender={"wm2": light_value},
    )


def update_voltage(voltage_value):
    dispatcher.send(
        signal="broadcast_battery",
        sender={"voltage": voltage_value},
    )


def update_wind(speed_value, direction_value):
    dispatcher.send(
        signal="broadcast_wind",
        sender={"wind_speed": speed_value, "wind_dir": direction_value},
    )


def update_temp_rh(humi_value, temp_value, offset_h_value, offset_t_value):
    dispatcher.send(
        signal="broadcast_serial",
        sender={
            "current_humidity": humi_value,
            "current_temperature": temp_value,
            "offset_h": offset_h_value,
            "offset_t": offset_t_value,
        },
    )


def update_temp_rh_offset(offset_h_value, offset_t_value):
    dispatcher.send(
        signal="set_offset",
        sender={"hum_offset": offset_h_value, "temp_offset": offset_t_value},
    )


def update_temp_sensor_connection_status(status, col):
    dispatcher.send(signal="set_temp_status", sender={"status": status, "col": col})


def update_light_sensor_connection_status(status, col):
    dispatcher.send(signal="set_light_status", sender={"status": status, "col": col})


def update_usb_status(is_inserted):
    dispatcher.send(
        signal="usb_is_inserted",
        sender=is_inserted,
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


def refresh_data_box():
    dispatcher.send(
        signal="refresh_file_data",
        sender="output",
    )


def toggle_data_logging(message):
    dispatcher.send(signal="toggle_logging", sender={"msg": message})


def shutdown_device():
    dispatcher.send(
        signal="shutdown_signal",
        sender="shutdown",
    )
