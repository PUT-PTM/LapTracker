import ptvsd
import gpsd
import csv
import RPi.GPIO as GPIO
import time
import glob,os
import Display
from Distance import equirectangular_dist_approx
from LineIntersection import intersects
from Display import DisplaySetter

class Tracker(object):

    def __init__(self):
        gpsd.connect()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3,  GPIO.IN) #physical pull up resistor is fitted on this channel
        GPIO.add_event_detect(3, GPIO.BOTH, callback=self.button_callback)
        

        self.display = DisplaySetter()
        self.display.printmenu() 

        self.tracking = False
        self.running = True
        self.start = None
        self.finish_p1 = None
        self.finish_p2 = None

    def set_point(self):
        packet = gpsd.get_current()
        if(self.finish_p1 is None):
            self.finish_p1 = (packet.lon, packet.lat)
            print("Finish point 1 setted")
        else:
            print("Finish point 2 setted")
            self.finish_p2 = self.finish_p1
            print("Finish point 1 setted")
            self.finish_p1 = (packet.lon, packet.lat)

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
        self.packet = gpsd.get_current()
        while self.running:
                time.sleep(.9)
                if self.finish_p1 is None or self.finish_p2 is None:
                    continue
                packet = gpsd.get_current()
                distance = equirectangular_dist_approx(packet.lon, packet.lat, self.packet.lon, self.packet.lat)
                #print("Distance haver: " + str(distance_haver) + " Distance equire: " + str(distance_equire))
                last_p = (self.packet.lat, self.packet.lon)
                actual_p = (packet.lat, packet.lon)

                       
                self.display.printspeed()
                self.display.printsubmenu()
                self.display.printsignalbar()
                self.display.setspeed(int(packet.hspeed*3.6))
                self.display.setdistance(int(distance))
                self.display.printcurrentposition()
                self.display.disp.image(self.display.image)
                self.display.disp.display()
                self.display.nextscreen()
                
                R  = intersects((self.finish_p1 ,self.finish_p2), (last_p, actual_p))
                self.packet = packet

                if R:
                    print ("Distance to finish: {:0.1f}m Intersection detected!".format(distance))
                else:
                    print ("Distance to finish: {:0.1f}m".format(distance))

        path = 'sudo shutdown -h now '
        os.system (path)

#ptvsd.enable_attach(secret='my_secret')
#ptvsd.wait_for_attach()


tracker = Tracker()
tracker.run()

