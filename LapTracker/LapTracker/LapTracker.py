import ptvsd
import gpsd
import csv
import RPi.GPIO as GPIO
import time
import glob,os

class Tracker(object):

    def __init__(self):
        gpsd.connect()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3,  GPIO.IN) #physical pull up resistor is fitted on this channel
        GPIO.add_event_detect(3, GPIO.BOTH, callback=self.button_callback)
        self.recording = False
        self.running = True
        self.start = None

    def button_callback(self, channel):
        if GPIO.input(3) == 0 and self.start is None:
            self.start = time.time()
        if GPIO.input(3) == 1 and self.start is not None:
            print("high")
            end = time.time()
            elapsed = end - self.start
            print(elapsed)

            self.start = None
        
            if(elapsed<1):
                print("Click")
            else:
                print("Long click")
        #if(channel == 18):
        #    self.recording = not self.recording
        #elif(channel == 3):
        #    self.running = not self.running

    def run(self):
        while self.running:
            if(self.recording):
                self.record()
            time.sleep(1)
        time.sleep(5)
        path = 'sudo shutdown -h now '
        os.system (path)

    def record(self):
        os.chdir('/home/pi/data')
        i = 0
        for file in glob.glob("*.csv"):
            x = int(filter(str.isdigit, file))
            if(i<=x):
                i=x+1
        file_name = 'data{0}.csv'.format(i)
        print(file_name)
        with open(os.path.join('/home/pi/data', file_name),'wb') as out:
            csv_out=csv.writer(out)

            while self.recording:
                packet = gpsd.get_current()
                csv_out.writerow([str(packet.lat), str(packet.lon), str(packet.time)])
                time.sleep(1)

#ptvsd.enable_attach(secret='my_secret')
#ptvsd.wait_for_attach()

tracker = Tracker()
tracker.run()

