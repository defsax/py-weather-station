import serial
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
