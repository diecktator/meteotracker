from gps3 import gps3
import pprint
import json
import bme280
import os
import sys
import time
from sensorhub.hub import SensorHub
from pymongo import MongoClient, GEO2D, GEOSPHERE

c = MongoClient()
db_name = os.environ.get("MONGODB_DATABASE_NAME")
if db_name == None:
    print("Please provide the MongoDB database name as a environment variable MONGODB_DATABASE_NAME:")
    print("MONGODB_DATABASE_NAME=foo python3 logger.py")
    sys.exit(1)
db = c.foo
db.locations.create_index([("geometry", GEOSPHERE)])

hub = SensorHub()

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        if data_stream.TPV["lat"] != "n/a" and data_stream.TPV["lon"] != "n/a":
            fieldsToZero = ["epc", "epd", "epy", "epv", "eps", "climb", "alt", "track", "epx", "ept"]
            for i in fieldsToZero:
                if data_stream.TPV[i] == "n/a":
                    data_stream.TPV[i] = -12000

            data_stream.TPV['temp'] = hub.get_off_board_temperature()
            data_stream.TPV['pressure'] = hub.get_barometer_pressure()
            data_stream.TPV["humidity"] = hub.get_humidity()
            data_stream.TPV["brightness"] = hub.get_brightness()

            location = { "type": "Feature", "geometry": {"type": "Point", "coordinates": [data_stream.TPV["lon"], data_stream.TPV["lat"]]}, "properties": data_stream.TPV }
            print(location)
            db.locations.insert_one(location)
            time.sleep(2)

