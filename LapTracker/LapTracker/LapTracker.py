import ptvsd
import gpsd
import RPi.GPIO as GPIO
import time
import glob,os
import datetime

from Distance import calculate_distance
from LineIntersection import intersects
from Display import DisplaySetter
from OutOfTrack import OutOfTrack

class Tracker(object):

    def __init__(self):
        gpsd.connect()

        self.start = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3,  GPIO.IN) #physical pull up resistor is fitted on this channel
        GPIO.setup(26,  GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        GPIO.add_event_detect(3, GPIO.BOTH, callback=self.button_callback)
        GPIO.add_event_detect(26, GPIO.BOTH, callback=self.button_callback)
        
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
            else:
                self.finish_p2 = self.finish_p1
                self.finish_p1 = (packet.lat, packet.lon)

                self.finish_center_p  = ((self.finish_p2[0] + self.finish_p1[0]) / 2, (self.finish_p2[1] + self.finish_p1[1]) / 2)

                #self.finish_center_p.lat  = self.finish_p1[0]
                #self.finish_center_p.lon  = self.finish_p1[1]
            self.display.pushalert("Point is set")
        else:
            self.display.pushalert("No GPS")

    def button_callback(self, channel):
        if GPIO.input(channel) == 0 and self.start is None:
            self.start = time.time()
        elif GPIO.input(channel) == 1 and self.start is not None:
            end = time.time()
            elapsed = end - self.start

            self.start = None
            
            if channel == 3:
                if(elapsed<1):
                    self.set_point()
                else:
                    self.running = not self.running
            elif channel == 26:
                self.display.nextscreen()
    def run(self):
        previous_packet = None
        start_time = None
        total_distance = 0
        min_distance = 40
        max_speed = 0
        speed = 0
        gps_signal = False
        lap_number = 0
        best_lap_time = datetime.timedelta(seconds=0)

        router = OutOfTrack()

        measureDelay = 1
        timepointA = time.monotonic();

        while self.running:
            timepointB = time.monotonic()
            if(timepointB-timepointA >= measureDelay):
                #print("Minelo ", measureDelay, " sekund.\n")
                timepointA = timepointB

                alert = "Lap {0}".format(lap_number)
                packet = gpsd.get_current()
                if packet.mode > 1:
                    gps_signal = True
                    
                    #is finish line setted
                    if self.finish_p1 is not None and self.finish_p2 is not None:

                        if(previous_packet is None):
                            previous_packet = packet
                        
                        speed = int(packet.hspeed*3.6)
                        if max_speed < speed:
                            max_speed = speed

                        distance_between_packets = calculate_distance(packet.lon, packet.lat, previous_packet.lon, previous_packet.lat)
                        if speed >= 2:
                            total_distance += distance_between_packets

                        #points for comparing track
                        router.add_p((packet.lat,packet.lon))

                        if lap_number >= 2:
                            on_track = router.check((packet.lat,packet.lon),0.00007)
                            if not on_track:
                                self.display.pushalert('out of track')

                        distance_to_finish = calculate_distance(packet.lon, packet.lat, self.finish_center_p[1], self.finish_center_p[0])


                        
                        if distance_to_finish < min_distance:
                            last_p = (previous_packet.lat, previous_packet.lon)
                            actual_p = (packet.lat, packet.lon)

                            interesction_p  = intersects((self.finish_p1, self.finish_p2), (last_p, actual_p))

                            if interesction_p is not None:
                                self.display.pushalert("New Lap")
                                lap_number+=1
                                router.new_lap()

                                distance_after_intersection = calculate_distance(packet.lon, packet.lat, interesction_p[1], interesction_p[0])
                                #print ("Distance to finish: {:0.1f}m Intersection detected!".format(distance_to_finish))
                                #print("Distance from intersection: {:0.1f}m".format(distance_after_intersection))

                                time_to_subtract = distance_after_intersection/distance_between_packets

                                actual_time = packet.get_time() 
                                actual_time-= datetime.timedelta(seconds=time_to_subtract)

                                if(lap_number >= 2):
                                    lap_time = actual_time - start_time 
                                    self.display.pushalert(lap_time)
                                    #print(lap_time)
                                    if lap_time<best_lap_time or lap_number ==2:
                                        best_lap_time = lap_time

                                start_time = actual_time

                            #else:
                                #print ("Distance to finish: {:0.1f}m".format(distance_to_finish))

                        previous_packet = packet
                    else:
                        self.display.pushalert("Set finish")
                else:
                    gps_signal = False
                    #print("No GPS fix")
                

                self.display.setspeed(speed)
                self.display.setdistance(total_distance)
                self.display.setbestlaptime(best_lap_time)
                self.display.setlapnumber(lap_number)
                self.display.setvmax(max_speed)
                self.display.setsignalbar(gps_signal)
                
                self.display.show()

                sleepTime = (measureDelay -0.1 -(time.monotonic()-timepointB)*2)
                if( sleepTime > 0):
                    time.sleep(sleepTime)
                 #print("Przespalem ", sleepTime, " sekund.\n")

        path = 'sudo shutdown -h now '
        os.system (path)

#ptvsd.enable_attach(secret='my_secret')
#ptvsd.wait_for_attach()

tracker = Tracker()
tracker.run()

