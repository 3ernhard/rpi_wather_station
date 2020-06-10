#!/usr/bin/env python3

import serial


previous_reading = -999


def read_celsius(port='/dev/ttyACM0', baudrate=9600, timeout=1):
    global preprevious_reading
    try:
        reading = float(serial.Serial(**locals()).readline())
    except serial.serialutil.SerialException:
        reading = previous_reading
        print()
    prereading = previous_reading
    return reading


if __name__ == '__main__':
    print(read_celsius(), '°C')
