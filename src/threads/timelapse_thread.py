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
                    "time,humidity,temperature,light,wind_speed,wind_dir,mission_id,voltage\n"
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
        voltage = str(self.sensor_manager.phidget_thread.battery_voltage_reading)
        light_average = str(self.sensor_manager.phidget_thread.getAverageLight())
        temp_average = str(self.sensor_manager.t_rh_thread.getAverageTemp())
        rh_average = str(self.sensor_manager.t_rh_thread.getAverageRH())
        wind_speed_average = str(self.sensor_manager.getAverageSpeed())
        wind_dir = str(self.sensor_manager.wind_dir)

        try:
            t = datetime.now()
            date_time = t.strftime("%m-%d-%Y_%H-%M-%S")
            with open(self.path + self.file_name, "a") as f:
                f.write(date_time + ",")
                f.write(rh_average + ",")
                f.write(temp_average + ",")
                f.write(light_average + ",")
                f.write(wind_speed_average + ",")
                f.write(wind_dir + ",")
                f.write(self.mission_id + ",")
                f.write(voltage)
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
        self.sensor_manager.phidget_thread.clearAverages()
        self.sensor_manager.t_rh_thread.clearAverages()
        self.sensor_manager.clearAverages()
        self.exit_flag.set()
