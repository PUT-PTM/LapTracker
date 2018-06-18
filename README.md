# LapTracker

### Overview:
LapTracker is a device that allows you to measure the time in which you have beaten the track, and the subsequent laps.
The main goal was to make it usable on a dirtbike or during extreme sports where cheaper alternative to expensive trackers is desired.

### Description:
There's a lot of trackers designed for sport activities and devices like smartwatches, smartphones (applications like Edomondo or Strava) that employ a gps module, but they all face the same issue - they can't tell when a route is repeating itself, when someone is beginning another lap on the same fixed track. There's also a matter of price - our goal is to create a cheap device that is good enough for amateur use, that isn't too expensive to worry about using it in extreme conditions and that will allow you to fully enjoy your favorite sport.
The only thing you will have to do is set your virtual finishing-line on the route, record a trial run (or choose from available ones, a planned feature for now) and then you are free to enjoy your sport while being able to get some useful data about your achievements without outsider's help or expensive devices.
Among the data our tracker provides there is: time in which you finished your lap, distance covered, maximal speed, actual speed.


Project's components:<br />
-Raspberry Pi Zero W <br />
-NEO-7M-C GPS/GLONASS module <br />
-PCD8544 (Nokia 5110) display <br />
-Powerbank 2000MAh <br />
-2x Push Buttons <br />
- Metal case  <br />

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

PCD8544 (Nokia 5110) display:<br />
GND-->GND<br />
VCC-->3.3V<br />
CLK-->SCLK<br />
DIN-->MOSI<br />
DC-->P16<br />
CE-->CE0_N<br />
RST-->P18<br /><br />

Turn the device on by pushing the button. Afterwards wait for the GPS module to catch the signal. A GPS icon will appear on the screen when it did.
When you are on the track, create the virtual finish-line by pressing the left button once for each of the two adjacent sides of the track. Now you should make one test lap to let the device learn the whole route (predefined routes are planned future feature) and afterwards you can enjoy the tracker to your heart's content. Right button toggles the various menus.

### How to compile:
 	
### Possible future features:
    - the possibility of saving and uploading recorded tracks<br />
    - downloadable tracks with best time rankings<br />
    - mobile application<br />

### Attributions:
https://pypi.python.org/pypi/gpsd-py3 - gpsd module<br />
https://pypi.python.org/pypi/RPi.GPIO - GPIO module<br />
https://1drv.ms/t/s!Ah7Mn0var0GvheVgGBCcdYaONGrsCg - Adafruit module<br />

### License:
Distributed under MIT license

### Credits:
* **Filip Wicha** - [filipwicha](https://github.com/filipwicha)
* **Marcin Wiktorowski** - [wiktorowski211](https://github.com/wiktorowski211)
* **Robert Zaranek** - [Rzar8767](https://github.com/Rzar8767)



The project was conducted during the Microprocessor Lab course held by the Institute of Control and Information Engineering, Poznan University of Technology.<br />
Supervisor: Tomasz Mańkowski
