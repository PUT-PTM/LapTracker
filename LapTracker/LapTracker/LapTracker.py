import ptvsd
import gpsd
import RPi.GPIO as GPIO
import time
import glob,os

from Distance import calculate_distance
from LineIntersection import intersects
from Display import DisplaySetter

class Tracker(object):

    def __init__(self):
        gpsd.connect()

        self.start = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3,  GPIO.IN) #physical pull up resistor is fitted on this channel
        GPIO.add_event_detect(3, GPIO.BOTH, callback=self.button_callback)
        
        self.display = DisplaySetter()
        self.display.printmenu() 

        self.tracking = False
        self.running = True

        self.finish_p1 = None
        self.finish_p2 = None
        self.finish_center_p = None

        self.start_time = None

        self.distance = 0
        self.min_distance = 0

    def set_point(self):
        packet = gpsd.get_current()
        if packet.mode > 1:
            if(self.finish_p1 is None):
                self.finish_p1 = (packet.lat, packet.lon)
                print("Finish point 1 setted")
            else:
                print("Finish point 2 setted")
                self.finish_p2 = self.finish_p1
                print("Finish point 1 setted")
                self.finish_p1 = (packet.lat, packet.lon)

                self.finish_center_p = packet
                self.finish_center_p.lat  = (self.finish_p2[0] + self.finish_p1[0]) / 2
                self.finish_center_p.lon  = (self.finish_p2[1] + self.finish_p1[1]) / 2

                self.min_distance = 5 * calculate_distance(packet.lon, packet.lat, self.finish_center_p.lon, self.finish_center_p.lat)
        else:
            print("No GPS fix")

    def button_callback(self, channel):
        if GPIO.input(3) == 0 and self.start is None:
            self.start = time.time()
        elif GPIO.input(3) == 1 and self.start is not None:
            print("high")
            end = time.time()
            elapsed = end - self.start
            print(elapsed)

            self.start = None
        
            if(elapsed<1):
                self.set_point()
            else:
                self.running = not self.running

    def run(self):
        while self.running:
                time.sleep(.9)
                if self.finish_p1 is None or self.finish_p2 is None or self.finish_center_p is None:
                    continue
                packet = gpsd.get_current()
                if packet.mode > 1:
                    if(self.packet is None):
                        self.packet = packet
                        continue
                
                    self.distance += calculate_distance(packet.lon, packet.lat, self.packet.lon, self.packet.lat)

                    distance_to_finish = calculate_distance(packet.lon, packet.lat, self.finish_center_p.lon, self.finish_center_p.lat)

                    if distance_to_finish < self.min_distance:

                        last_p = (self.packet.lat, self.packet.lon)
                        actual_p = (packet.lat, packet.lon)

                        interesction_p  = intersects((self.finish_p1, self.finish_p2), (last_p, actual_p))

                        if interesction_p is not None:
                            print ("Distance to finish: {:0.1f}m Intersection detected!".format(distance_to_finish))

                            actual_time = packet.get_time()
                            if(self.start_time is not None):
                                lap_time = actual_time - self.start_time
                            self.start_time = actual_time

                        else:
                            print ("Distance to finish: {:0.1f}m".format(distance_to_finish))

                    self.display.printspeed()
                    self.display.printsubmenu()
                    self.display.printsignalbar()
                    self.display.setspeed(int(packet.hspeed*3.6))
                    self.display.setdistance(int(self.distance))
                    self.display.printcurrentposition()
                    self.display.disp.image(self.display.image)
                    self.display.disp.display()
                    #self.display.nextscreen()

                    self.packet = packet

                else:
                    print("No GPS fix")

        path = 'sudo shutdown -h now '
        os.system (path)

#ptvsd.enable_attach(secret='my_secret')
#ptvsd.wait_for_attach()

tracker = Tracker()
tracker.run()

