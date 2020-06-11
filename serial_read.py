#!/usr/bin/env python3

import serial
import time


def read_celsius(port='/dev/ttyACM0', baudrate=9600):
    while True:
        try:
            s = serial.Serial(port, baudrate)
            s.write(1)
            return float(s.readline())
        except:
            time.sleep(0.1)


if __name__ == '__main__':
    print(read_celsius(), '°C')
