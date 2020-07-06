#!/usr/bin/env python3

from datetime import datetime
from time import sleep
from subprocess import call
import os
import numpy as np

from BME280 import BME280
from serial_read import read_celsius


BIN_SIZE = 300
STEP_SIZE = 10
# in seconds (int)
METHOD = np.median

LED = "OFF"


sensor = BME280()
time_str = "%Y-%m-%dT%H:%M:%S"
file_path = os.path.dirname(os.path.realpath(__file__))
F = file_path
F += "/data/"
F += datetime.now().strftime(time_str.replace(":", "-"))
F += ".csv"


def go_dark(force=False):
    """ Turn of RPI LEDs"""
    global LED
    if force or LED != "OFF" :
        call(file_path+"/go-dark")
        LED = "OFF"


def go_green(force=False):
    """ Turn on RPI's green LED"""
    global LED
    if force or LED != "GREEN":
        go_dark(force=True)
        call(file_path+"/go-green")
        LED = "GREEN"


def go_red(force=False):
    """ Turn on RPI's red LED"""
    global LED
    if force or LED != "RED" :
        go_dark(force=True)
        call(file_path+"/go-red")
        LED = "RED"


with open(F, "w") as csv:
    csv.write("#time,t_outside,t_inside,pressure,humidity\n")
    csv.write(f"#{time_str},°C,°C,hPa,%\n")


if __name__ == '__main__':

    go_dark(force=True)

    i = 0
    # build METHOD over BIN_SIZE, record every STEP_SIZE seconds
    t_outside = []
    t_inside = []
    pressure = []
    humidity = []

    while sensor.refresh():

        t_outside.append(read_celsius())
        t_inside.append(sensor.temperature)
        pressure.append(sensor.pressure)
        humidity.append(sensor.humidity)

        if i >= BIN_SIZE:

            t_outside = METHOD(t_outside)
            t_inside = METHOD(t_inside)
            pressure = METHOD(pressure)
            humidity = METHOD(humidity)

            with open(F, "a") as csv:
                csv.write(datetime.now().strftime(f"{time_str},{t_outside:g},{t_inside:g},{pressure:g},{humidity:g}\n"))

            # Wenn die Aussentemperatur in einem +- n°C Bereich liegt: grün
            if abs(t_inside - t_outside) <= 1:
                go_green()
            # Wenn nicht und die Aussentemperatur größer als die Innentemperatur ist: rot
            elif t_inside <= t_outside;
                go_red()
            # Sonst aus (Aussentemperatur kleiner als Innentemperatur)
            else:
                go_dark()

            i = 0
            t_outside = []
            t_inside = []
            pressure = []
            humidity = []

        else:
            i += STEP_SIZE

        sleep(STEP_SIZE)
