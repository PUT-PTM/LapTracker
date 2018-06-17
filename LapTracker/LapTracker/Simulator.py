import csv
import threading
import time
import sys
from Distance import *
from LineIntersection import *
from OutOfTrack import *

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
            print("EOF ##############################################################")
            input()
            self.file.seek(0)
            return self.get_current()

#router = OutOfTrack('Tracks/lap.csv')
#sim = Simulator()

#packet1 = sim.get_current()
#while True:
#    packet2 = sim.get_current()
#    R = router.check((packet2.lat,packet2.lon),0.00007)
#    packet1 = packet2
#    if R:
#        print ("Found")
#    else:
#        print ("Not found")
#    if(packet1.date == "BAD"):
#         input()

sim = Simulator()
finish = Packet(52.323486, 17.668115, '')
A = (52.323632, 17.668220)
B = (52.323384, 17.668048)
packet1 = sim.get_current()

# how long we wait between subsequent tracking, in seconds
#this part before tracking starts
measureDelay = 1.0
timepointA = time.monotonic();

while True:
    # this is the main loop of the tracker
    timepointB = time.monotonic()
      # in here all the per-tracking-loop logic
    if(timepointB-timepointA >= measureDelay):
        print("Minelo ", measureDelay, " sekund.\n")
        timepointA = timepointB
        packet2 = sim.get_current()
        #distance_haver = haversine(packet1.lon, packet1.lat, finish.lon, finish.lat)
        distance = calculate_distance(packet1.lon, packet1.lat, finish.lon, finish.lat)
    
        #print("Distance haver: " + str(distance_haver) + " Distance equire: " + str(distance_equire))
        C = (packet1.lat, packet1.lon)
        D = (packet2.lat, packet2.lon)
        R  = intersects((A,B),(C,D))
        packet1 = packet2
        if R:
            print ("Distance to finish: {:0.1f}m Intersection detected!".format(distance))
        else:
            print ("Distance to finish: {:0.1f}m".format(distance))
            time.sleep(0.03)
        if distance < 15:
            time.sleep(0.4)
        #at the end of per-tracking-loop logic
        #the value here can be tweaked, the whole part is just to save battery life
        sleepTime = (measureDelay -0.1 -(time.monotonic()-timepointB)*2)
        if( sleepTime > 0):
         time.sleep(sleepTime)
         print("Przespalem ", sleepTime, " sekund.\n")


# TEMPLATE TO BE PUT INTO LapTracker.py
# how long we wait between subsequent tracking, in seconds
#this part before tracking starts
#measureDelay = 2.0
#timepointA = time.monotonic();

# this is the main loop of the tracker
#while(True):
#    timepointB = time.monotonic()
#    # in here all the per-tracking-loop logic
#    if(timepointB-timepointA >= measureDelay):
#        print("Minelo ", measureDelay, " sekund.\n")
#        timepointA += timepointB - timepointA
#
#        #at the end of per-tracking-loop logic
#        #the value here can be tweaked, the whole part is just to save battery life
#        sleepTime = (measureDelay -0.1 -(time.monotonic()-timepointB)*2)
#        if( sleepTime > 0):
#         time.sleep(sleepTime)
#         print("Przespalem ", sleepTime, " sekund.\n")