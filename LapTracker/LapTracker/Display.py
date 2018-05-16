import time
import math
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Set fonts
font_speed = ImageFont.truetype('pixelmix.ttf', 28)
font_kmh = ImageFont.truetype('pixelmix.ttf', 8)
font_parameter = ImageFont.truetype('pixelmix.ttf', 16)

class DisplaySetter(object):
    ## Raspberry Pi hardware SPI config:
    DC = 23
    RST = 24
    SPI_PORT = 0
    SPI_DEVICE = 0

    # Hardware SPI usage:
    disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

    draw = ImageDraw.Draw(image)

    def __init__(self):
        # Initialize library.
        self.disp.begin(contrast=50)
        
        # Clear display
        self.disp.clear()
        self.disp.display()
        
        # Draw a white filled box to clear the image
        self.draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
    
    # Variables in use
    speed = 85
    distance = 10.3
    laptime = 430.0
    screen = 0  # flag that informs which screen to show (for example: distance, time, etc)
    signalbar = False # true if there is signal, false otherwise
    currentposition = False # false if you have to speed up, true if you are faster than before

    def printmenu(self):
        # km/h
        self.draw.text((62, 17), 'km/h', font=font_kmh)

        # left menu (rectangle)
        self.draw.line((13, 0, 13, 47), fill=0)
        self.draw.line((0, 0, 0, 47), fill=0)
        self.draw.line((0, 0, 13, 0), fill=0)
        self.draw.line((0, 47, 13, 47), fill=0)

        # left menu (?shelves?)
        self.draw.line((0, 12, 13, 12), fill=0)
        self.draw.line((0, 24, 13, 24), fill=0)
        self.draw.line((0, 36, 13, 36), fill=0)
	
	    #print letters in submenu
        self.draw.text((4, 2), 'S', font=font_kmh)
        self.draw.text((4, 14), 'T', font=font_kmh)
        self.draw.text((4, 26), 'L', font=font_kmh)
        self.draw.line((6, 39, 6, 44), fill=0)


    def printspeed(self):
        # Clear the speed
        self.draw.rectangle((17, 0, 61, 28), outline=255, fill=255)

        # Print the speed
        self.draw.text((17, -3), str(self.speed), font=font_speed)

        ## Test of speed
        #self.speed += 5
        #if self.speed > 80:
        #    self.speed = 1
        ## End of the test
        return

    def nextscreen(self):
        #Changes the flag of a screen after clicking the button
        self.screen += 1
        if self.screen == 4:
            self.screen = 0
	
	    #Lines below print currently chosen submenu
        if self.screen == 0:
            self.draw.rectangle((1, 1, 12, 11), outline=0, fill=255)
            self.draw.rectangle((1, 37, 12, 46), outline=255, fill=255)
            self.draw.text((4, 2), 'S', font=font_kmh)
            self.draw.line((6, 39, 6, 44), fill=0)
        elif self.screen == 1:
            self.draw.rectangle((1, 1, 12, 11), outline=255, fill=255)
            self.draw.rectangle((1, 13, 12, 23), outline=0, fill=255)
            self.draw.text((4, 14), 'T', font=font_kmh)
            self.draw.text((4, 2), 'S', font=font_kmh)
        elif self.screen == 2:
            self.draw.rectangle((1, 13, 12, 23), outline=255, fill=255)
            self.draw.rectangle((1, 25, 12, 35), outline=0, fill=255)
            self.draw.text((4, 26), 'L', font=font_kmh)
            self.draw.text((4, 14), 'T', font=font_kmh)
        elif self.screen == 3:
            self.draw.rectangle((1, 25, 12, 35), outline=255, fill=255)
            self.draw.rectangle((1, 37, 12, 46), outline=0, fill=255)
            self.draw.line((6, 39, 6, 44), fill=0)
            self.draw.text((4, 26), 'L', font=font_kmh)


    def printdistance(self):
	    ## Used for test
        #self.distance+=0.25
	    #if self.distance > 99:
		   # self.distance -= 99
		
        # Clear the display
	    self.draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
	    self.draw.text((70, 35), 'km', font=font_kmh)
        # Print the distance
	    self.draw.text((17, 28), str(self.distance), font=font_parameter)

    def printlaptime(self):
        # Clear the display
	    self.draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
	    self.draw.text((75, 35), 's', font=font_kmh)
        # Print lap time
	    self.draw.text((17, 28), str(self.laptime), font=font_parameter)
	
    def something1(self):
        # Clear the display
	    self.draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
	    self.draw.text((70, 35), '', font=font_kmh)
        # Print sth
	    self.draw.text((17, 28), str('sth :('), font=font_parameter)

    def something2(self):
        # Clear the display
	    self.draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
	    self.draw.text((70, 35), '', font=font_kmh)
        # Print sth
	    self.draw.text((17, 28), str('sth :)'), font=font_parameter)

    def printsubmenu(self):
	    if self.screen == 0:
		    self.printdistance()
	    elif self.screen == 1:
		    self.printlaptime()
	    elif self.screen == 2:
		    self.something1()
	    else:
		    self.something2()

    def printsignalbar(self): #prints gps signal
        if self.signalbar == True:
            self.draw.rectangle((62, 0, 69, 8), outline=255, fill=255)
            self.draw.rectangle((62, 4, 63, 8), outline=0, fill=0)
            self.draw.rectangle((65, 2, 66, 8), outline=0, fill=0)
            self.draw.rectangle((68, 0, 69, 8), outline=0, fill=0)
        elif self.signalbar == False:
            self.draw.rectangle((62, 0, 69, 8), outline=255, fill=255)
            self.draw.text((64, 1), 'X', font=font_kmh)
        # Used for tests
        #self.signalbar = not self.signalbar

    def printcurrentposition(self): #prints information about current position
        if self.currentposition == False:
            self.draw.rectangle((72, 0, 83, 15), outline=255, fill=255)
            #draw SPEEDUP symbol
            self.draw.rectangle((76, 4, 79, 15), outline=0, fill=0)
            self.draw.line((73, 4, 82, 4), fill=0)
            self.draw.line((74, 3, 81, 3), fill=0)
            self.draw.line((75, 2, 80, 2), fill=0)
            self.draw.line((76, 1, 79, 1), fill=0)
            self.draw.line((77, 0, 78, 0), fill=0)
        elif self.currentposition == True:
            self.draw.rectangle((72, 0, 83, 15), outline=255, fill=255)    
            #draw SLOWDWON symbol
            self.draw.rectangle((76, 0, 79, 10), outline=0, fill=0)
            self.draw.line((73, 11, 82, 11), fill=0)
            self.draw.line((74, 12, 81, 12), fill=0)
            self.draw.line((75, 13, 80, 13), fill=0)
            self.draw.line((76, 14, 79, 14), fill=0)
            self.draw.line((77, 15, 78, 15), fill=0)
        
        # Used for test
        #self.currentposition = not self.currentposition

    # SETTERS for speed, distance, laptime
    # TOGGLERS for signalbar currentposition
    # TO TURN SWITCH TO NEXT SCREEN USE displayInUse.nextscreen()
    def setspeed(self, new):
        self.speed = new

    def setdistance(self, new):
        self.distance = new

    def setlaptime(self, new):
        self.laptime = new

    def togglesignalbar(self):
        self.signalbar = not self.signalbar

    def togglecurrentposition(self):
        self.currentposition = not self.currentposition


displayInUse = DisplaySetter()

print('It works (Press Ctrl+C to stop)')
displayInUse.printmenu()

while True:
	displayInUse.printspeed()
	displayInUse.printsubmenu()
	displayInUse.printsignalbar()
	displayInUse.printcurrentposition()
	displayInUse.disp.image(displayInUse.image)
	displayInUse.disp.display()
	displayInUse.nextscreen() # Used to tests
	time.sleep(1)