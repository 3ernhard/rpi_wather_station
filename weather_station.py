#!/usr/bin/env python3

from datetime import datetime
from time import sleep
import os

from BME280 import BME280
from serial_read import read_celsius


BIN_SIZE = 60
# in seconds (int)


sensor = BME280()
time_str = "%Y-%m-%dT%H:%M:%S"
F = os.path.dirname(os.path.realpath(__file__))
F += "/data/"
F += datetime.now().strftime(time_str.replace(":", "-"))
F += ".csv"


with open(F, "w") as csv:
    csv.write("#time,t_outside,t_inside,pressure,humidity\n")
    csv.write(f"#{time_str},°C,°C,hPa,%\n")


# build average over BIN_SIZE, record every second
i = t_outside = t_inside = pressure = humidity = 0
while sensor.refresh():

    t_outside += read_celsius()
    t_inside  += sensor.temperature
    pressure  += sensor.pressure
    humidity  += sensor.humidity

    if i == BIN_SIZE:
        t_outside /= BIN_SIZE
        t_inside  /= BIN_SIZE
        pressure  /= BIN_SIZE
        humidity  /= BIN_SIZE
        with open(F, "a") as csv:
            csv.write(datetime.now().strftime(f"{time_str},{t_outside:g},{t_inside:g},{pressure:g},{humidity:g}\n"))
        i = t_outside = t_inside = pressure = humidity = 0
    else:
        i += 1

    sleep(1)
