import csv
import threading
import time

class Simulator(object):
    def __init__(self):
        self.file = open('Tracks/gpsdata.csv','rt')
        self.rows = csv.reader(self.file)

    def __del__(self):
        self.file.close()

    def get_row(self):
        first = next(self.rows, None)
        if first:
            print (first)
            time.sleep(1)
        else:
            self.file.seek(0)

sim = Simulator()
while True:
    sim.get_row()
