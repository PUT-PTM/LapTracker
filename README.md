# LapTracker

### Overview:
LapTracker is a project which enables to track lap times on dirtbike, bike, car or whatever you want. 

### Description:
There's lot of gps trackers for sports activities - smartwatches with gps, or smartphone applications like Endomondo or Strava, but they are facing the same problem. They can't track laps on fixed distance track, and usually are too expensive to use in extreme conditions.
LapTracker is created to resolve this problem. You can set your virtual start/finish line and everytime you cross this line, it will save lap time.

Projects components:<br />
-Raspberry Pi Zero W <br />
-NEO-7M-C GPS/GLONASS module <br />
-PCD8544 (Nokia 3310) display <br />
-Powerbank 4000MAh <br />
-2x switch buttons <br />

### Tools: 
Visual Studio Community - Python with ptvsd module for remote debugging <br />
Putty - SSH connection <br />

### How to run:
#### Connections:<br />
NEO-7M-C GPS/GLONASS module:<br />
RxD-->P08<br />
TxD-->P10<br />
GND-->GND<br />
VCC-->5V<br /><br />

Turn on the device by switching button. When you're on the track just pick two points on both sides of the track that will act as the start/finish line.

### How to compile:
 	
### Future improvements:
Improvements:<br />
    -starts trainer<br />
    -best lap time rank<br />
    -mobile application analysis<br />

### Attributions:
https://pypi.python.org/pypi/gpsd-py3 - gpsd module<br />
https://pypi.python.org/pypi/RPi.GPIO - GPIO module<br />

### License:
Distributed under MIT license

### Credits:
* **Filip Wicha** - [filipwicha](https://github.com/filipwicha)
* **Marcin Wiktorowski** - [wiktorowski211](https://github.com/wiktorowski211)
* **Robert Zaranek** - [Rzar8767](https://github.com/Rzar8767)



The project was conducted during the Microprocessor Lab course held by the Institute of Control and Information Engineering, Poznan University of Technology.<br />
Supervisor: Tomasz Mañkowski
