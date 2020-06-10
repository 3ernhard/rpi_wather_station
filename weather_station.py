#!/usr/bin/env python3

from datetime import datetime
from time import sleep
import os

from BME280 import BME280
from serial_read import read_celsius

sensor = BME280()
time_str = "%Y-%m-%dT%H:%M:%S"
file = os.path.dirname(os.path.realpath(__file__))
file += "/data/"
file += datetime.now().strftime(time_str.replace(":", "-"))
file += ".csv"


with open(file, "w") as csv:
    csv.write("#time,t_outside,t_inside,pressure,humidity\n")
    csv.write(f"#{time_str},°C,°C,hPa,%\n")


while sensor.refresh():
    with open(file, "a") as csv:
        t_outside = read_celsius()
        csv.write(datetime.now().strftime(f"{time_str},{t_outside:g},{sensor.temperature:g},{sensor.pressure:g},{sensor.humidity:g}\n"))
    sleep(60)
