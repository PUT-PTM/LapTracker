import ptvsd
import gpsd
import csv
import RPi.GPIO as GPIO
import time
import glob,os
from Distance import *


class Measure(object):

    def __init__(self):
        gpsd.connect()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(3,  GPIO.IN) #physical pull up resistor is fitted on this channel
        GPIO.add_event_detect(18, GPIO.RISING, callback=self.button_callback, bouncetime=300)
        GPIO.add_event_detect(3, GPIO.FALLING, callback=self.button_callback, bouncetime=300)
        self.distance = 0
        self.running = True
        self.last_packet = None

    def button_callback(self, channel):
        if(channel == 18):
            self.measure()
        elif(channel == 3):
            self.running = not self.running
            
        print("Button clicked %d" % channel)

    def run(self):
        while self.running:
            time.sleep(1)
        time.sleep(5)
        path = 'sudo shutdown -h now '
        os.system (path)

    def measure(self):
        packet = gpsd.get_current()
        if(self.last_packet is not None):
            print("Point 2 setted")
            distance = equirectangular_dist_approx(packet.lon, packet.lat, self.last_packet.lon, self.last_packet.lat)
            self.distance += distance
            print("Distance = {:0.1f}m".format(distance))
            print("Total distance = {:0.1f}m".format(self.distance))
            self.last_packet = None
        else:
            print("Point 1 setted")
            self.last_packet = packet

#ptvsd.enable_attach(secret='my_secret')
#ptvsd.wait_for_attach()

measure = Measure()
measure.run()

