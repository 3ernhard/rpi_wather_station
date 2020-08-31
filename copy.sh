#!/bin/sh

rsync -avz -- pi:/home/pi/weather_station/data/*.csv /home/bernhard/Projects/RPI/weather_station/data/
