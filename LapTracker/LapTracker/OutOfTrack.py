import csv

class OutOfTrack(object):

    def __init__(self, filepath):
        self.file = open(filepath,'rt')
        self.rows = csv.reader(self.file)
        self.coords = []
        for item in self.rows:
            self.coords.append((float(item[0]), float(item[1])))
        self.file.close()
        self.pos = 0

    def contains(self, point, approx):
        curpos = self.pos
        for routep in self.coords[self.pos:]:
            ++curpos
            if( abs(point[0] - routep[0]) <= approx and abs(point[1] - routep[1]) <= approx):
               self.pos = curpos
               return True
        curpos = self.pos
        if self.pos == 0:
            return False
        for routep in self.coords[0:self.pos-1]:
            --curpos
            if( abs(point[0] - routep[0]) <= approx and abs(point[1] - routep[1]) <= approx):
               self.pos = curpos
               return True
        return False


