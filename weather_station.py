#!/usr/bin/env python3

from datetime import datetime
from time import sleep

from BME280 import BME280

sensor = BME280()
time_str = "%Y-%m-%dT%H:%M:%S"
file = "/home/pi/Documents/weather_station/data/"
file += datetime.now().strftime(time_str.replace(":", "-"))
file += ".csv"


with open(file, "w") as csv:
    csv.write("#time,temperature,pressure,humidity\n")
    csv.write(f"#{time_str},°C,hPa,%\n")


while sensor.refresh():
    with open(file, "a") as csv:
        csv.write(datetime.now().strftime(f"{time_str},{sensor.temperature:g},{sensor.pressure:g},{sensor.humidity:g}\n"))
    sleep(60)
