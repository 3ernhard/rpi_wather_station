#!/bin/bash

service_file='/etc/systemd/system/weather_station.service'

if [ ! -f "$service_file" ]; then
	echo "[Unit]
Description=Weather Station
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/weather_station/weather_station.py
StandardInput=tty-force

[Install]
WantedBy=multi-user.target" > "$service_file"
else
	echo "'$service_file' already exists!"
fi

unset service_file
