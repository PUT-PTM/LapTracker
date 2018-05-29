import ptvsd
import gpsd
import csv
import time
import glob,os

class Recorder(object):

    def __init__(self):
        self.recording = False

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

#recorder = Recorder()
#recorder.record()


