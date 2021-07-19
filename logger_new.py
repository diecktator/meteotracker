import pprint
import json
import os
import sys
import time
import display
from Adafruit_BMP import BMP085

bmp = BMP085.BMP085()
temp = bmp.read_temperature()
pressure = bmp.read_pressure() / 100
altitude = round(bmp.read_altitude(), 2)

print(pressure, altitude, temp)

display.display(temp, pressure, altitude)
