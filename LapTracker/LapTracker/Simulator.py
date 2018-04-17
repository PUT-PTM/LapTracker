import csv
import threading
import time

from Distance import *

class Packet(object):
    def __init__(self, lat, lon, date):
        self.lat = float(lat)
        self.lon = float(lon)
        self.date = date

class Simulator(object):
    def __init__(self):
        self.file = open('Tracks/gpsdata.csv','rt')
        self.rows = csv.reader(self.file)

    def __del__(self):
        self.file.close()

    def get_current(self):
        row = next(self.rows, None)
        if row:
            packet = Packet(row[0],row[1],row[2])
            return packet
        else:
            self.file.seek(0)
            return self.get_current()

sim = Simulator()
while True:
    packet1 = sim.get_current()
    packet2 = sim.get_current()

    distance_haver = haversine(packet1.lon, packet1.lat, packet2.lon, packet2.lat)
    distance_equire = equirectangular_dist_approx(packet1.lon, packet1.lat, packet2.lon, packet2.lat)

    print("Distance haver: " + str(distance_haver) + " Distance equire: " + str(distance_equire))
    time.sleep(1)
