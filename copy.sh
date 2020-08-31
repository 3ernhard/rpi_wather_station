#!/bin/sh

# https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# is a useful one-liner which will give you the full directory name of the script no matter where it is being called from.

rsync -avz -- pi:/home/pi/weather_station/data/*.csv "$DIR/data/"

unset DIR
