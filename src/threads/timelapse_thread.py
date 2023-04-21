from threading import Event
from datetime import datetime
import os
from PyQt5.QtCore import QThread


class TimelapseThread(QThread):
    def __init__(self, sensor_manager):
        super(TimelapseThread, self).__init__()
        self.sensor_manager = sensor_manager

    def setup(self, mission_id):
        print("timelapse thread setup")
        self.mission_id = mission_id

        # get/set destination folder
        self.path = os.path.abspath("/home/pi/weather_station_data")

        # get and format date
        start = datetime.now()
        self.start_time = start.strftime("%m-%d-%Y_%H-%M-%S")

        # create file with mission id and date
        self.file_name = "/" + self.mission_id + "_" + self.start_time + ".csv"

        # write defaults (csv)
        try:
            with open(self.path + self.file_name, "a") as f:
                f.write(
                    "time,humidity,temperature,light,wind_speed,wind_dir,mission_id\n"
                )
                f.close()
        except:
            print("write setup error")

        self.exit_flag = Event()

    def check_sensor(self, arg):
        print("check sensor", arg)

    def log_data(self):
        # TODO: lock thread here just in case

        # log all data
        light = str(round(self.sensor_manager.phidget_thread.wm2, 4))
        temperature = str(self.sensor_manager.t_rh_thread.temp)
        rh = str(self.sensor_manager.t_rh_thread.rh)
        wind_speed = str(round(self.sensor_manager.wind_speed, 4))
        wind_dir = str(self.sensor_manager.wind_dir)

        print("\n\nlogging:\n")
        print("light:", light)
        print("temperature:", temperature)
        print("rh:", rh)
        print("wind speed:", wind_speed)
        print("wind direction:", wind_dir)
        print("name:", self.mission_id)
        print("\n")

        try:
            t = datetime.now()
            date_time = t.strftime("%m-%d-%Y_%H-%M-%S")
            with open(self.path + self.file_name, "a") as f:
                f.write(date_time + ",")
                f.write(rh + ",")
                f.write(temperature + ",")
                f.write(light + ",")
                f.write(wind_speed + ",")
                f.write(wind_dir + ",")
                f.write(self.mission_id)
                f.write("\n")
                f.close()
        except:
            print("write error")

    def run(self):
        while not self.exit_flag.wait(timeout=60):
            # ~ self.check_sensor("args")
            self.log_data()

    def stop(self):
        print("Timelapse thread stopping...")
        self.exit_flag.set()
