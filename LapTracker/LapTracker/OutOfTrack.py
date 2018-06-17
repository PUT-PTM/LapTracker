class OutOfTrack(object):

    def __init__(self):
        self.pos = 0
        self.coords = []
        self.actual_lap = []

    def add_p(self, point):
        self.actual_lap.append(point)

    def new_lap(self):
        self.coords = self.actual_lap
        self.actual_lap.clear()

    def check(self, point, approx):
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


