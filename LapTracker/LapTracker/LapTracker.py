import ptvsd
import gpsd
import RPi.GPIO as GPIO
import time
import glob,os
import datetime

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
        else:
            print("No GPS fix")

    def button_callback(self, channel):
        if GPIO.input(3) == 0 and self.start is None:
            self.start = time.time()
        elif GPIO.input(3) == 1 and self.start is not None:
            end = time.time()
            elapsed = end - self.start

            self.start = None
        
            if(elapsed<1):
                self.set_point()
            else:
                self.running = not self.running

    def run(self):
        previous_packet = None
        start_time = None
        total_distance = 0
        min_distance = 40
        max_speed = 0
        speed = 0
        gps_signal = False
        self.display.setscreen(3)

        while self.running:
                time.sleep(.9)

                alert = '--'
                if self.finish_p1 is not None and self.finish_p2 is not None:
                    packet = gpsd.get_current()
                    if packet.mode > 1:
                        gps_signal = True

                        if(previous_packet is None):
                            previous_packet = packet
                    
                        distance_between_packets = calculate_distance(packet.lon, packet.lat, previous_packet.lon, previous_packet.lat)
                        total_distance += distance_between_packets

                        distance_to_finish = calculate_distance(packet.lon, packet.lat, self.finish_center_p.lon, self.finish_center_p.lat)

                        speed = int(packet.hspeed*3.6)

                        if max_speed < speed:
                            max_speed = speed

                        if distance_to_finish < min_distance:

                            last_p = (previous_packet.lat, previous_packet.lon)
                            actual_p = (packet.lat, packet.lon)

                            interesction_p  = intersects((self.finish_p1, self.finish_p2), (last_p, actual_p))

                            if interesction_p is not None:
                                #print ("Distance to finish: {:0.1f}m Intersection detected!".format(distance_to_finish))

                                distance_after_intersection = calculate_distance(packet.lon, packet.lat, interesction_p[1], interesction_p[0])
                                #print("Distance from intersection: {:0.1f}m".format(distance_after_intersection))

                                time_to_subtract = distance_after_intersection/distance_between_packets

                                actual_time = packet.get_time() 
                                actual_time-= datetime.timedelta(seconds=time_to_subtract)

                                if(start_time is not None):
                                    lap_time = actual_time - start_time 
                                    alert = lap_time
                                    print(lap_time)
                                start_time = actual_time

                            else:
                                print ("Distance to finish: {:0.1f}m".format(distance_to_finish))

                        previous_packet = packet

                    else:
                        gps_signal = False
                        print("No GPS fix")
                else:
                    alert = "Set Finish"

                self.display.setspeed(speed)
                self.display.setdistance(total_distance)
                self.display.setsignalbar(gps_signal)
                self.display.setalert(alert)
                
                #if(alert is '--'):
                #    self.display.nextscreen()
                #else:
                #    self.display.setscreen(3)

                self.display.printspeed()
                self.display.printsubmenu()
                self.display.printsignalbar()
                self.display.printcurrentposition()
                self.display.disp.image(self.display.image)
                self.display.disp.display()

        path = 'sudo shutdown -h now '
        os.system (path)

#ptvsd.enable_attach(secret='my_secret')
#ptvsd.wait_for_attach()

tracker = Tracker()
tracker.run()

