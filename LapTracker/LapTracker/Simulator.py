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
finish = Packet(52.323239833,17.6696305, '')
while True:
    packet1 = sim.get_current()
    distance_haver = haversine(packet1.lon, packet1.lat, finish.lon, finish.lat)
    distance_equire = equirectangular_dist_approx(packet1.lon, packet1.lat, finish.lon, finish.lat)

    print("Distance haver: " + str(distance_haver) + " Distance equire: " + str(distance_equire))
    if distance_haver > 10:
        time.sleep(0.05)
    else:
        time.sleep(2)