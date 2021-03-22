#!/usr/bin/env bash

docker start mongo
killall gpsd
gpsd /dev/ttyACM0 -F /var/run/gpsd.sock
sleep 2
MONGODB_DATABASE_NAME=logger python3 /home/pi/code/logger/logger.py
