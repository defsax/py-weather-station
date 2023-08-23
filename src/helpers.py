import serial
import yaml
import sys
import os
import glob
from pydispatch import dispatcher
from PyQt5.QtCore import pyqtSlot


# return list
def list_serial_devices():
    ports = glob.glob("/dev/ttyACM[0-9]*")
    res = []
    for port in ports:
        try:
            s = serial.Serial(port)
            print(s)
            s.close()
            res.append(port)
        except:
            pass
    print(res)
    return res


# return one item
def get_t_rh_port():
    ports = glob.glob("/dev/ttyACM[0-9]*")
    res = ""
    for port in ports:
        res = port
        try:
            s = serial.Serial(port)
            s.close()
        except:
            pass
    print(res)
    return


@pyqtSlot(str, str)
def set_sensor_status(sensor, status, col):
    if sensor == "temp_rh":
        dispatcher.send(signal="set_temp_status", sender={"status": status, "col": col})
    if sensor == "light":
        dispatcher.send(
            signal="set_light_status", sender={"status": status, "col": col}
        )


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
        # print("sys._MEIPASS", base_path)
    except Exception:
        # base_path = os.path.abspath(".")
        # print("path.dirname(__file__)", os.path.dirname(__file__))
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)


def write_to_yaml(key, value):
    path = resource_path("settings.yml")
    try:
        # try:
        with open(path, "r+") as f:
            # load the content
            content = yaml.safe_load(f)
            # append the new id to the existing list
            content[key] = value
            # reset the position in the file (it's at the end since we read the file)
            f.seek(0)
            # write the updated YAML to the file
            yaml.dump(content, f, explicit_start=True, default_flow_style=False)
            # throw away any (old) content of the file after the current position,
            # which is at the end of the YAML we just wrote.
            # since we added more content, it's unlikely that there is more content here,
            # but not impossible!
            f.truncate()

    except:
        print("error writing to yaml")


def delete_files(loc):
    files = glob.glob(loc)
    for f in files:
        print("Removing", f, "...")
        os.remove(f)
