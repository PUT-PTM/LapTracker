
import ptvsd
import gpsd
import csv
import RPi.GPIO as GPIO
import time

ptvsd.enable_attach(secret='my_secret')
ptvsd.wait_for_attach()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

gpsd.connect() 

with open('data.csv','wb') as out:
    csv_out=csv.writer(out)

    while True:
        input_state = GPIO.input(18)
        packet = gpsd.get_current()
        csv_out.writerow([str(packet.lat), str(packet.lon), str(packet.time)])
        time.sleep(1)
        if input_state == False:
            break