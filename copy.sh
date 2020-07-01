#!/bin/sh

rsync -avz pi4:/home/pi/weather_station/data/*.csv /home/bernhard/Documents/RPI/weather_station/data/
