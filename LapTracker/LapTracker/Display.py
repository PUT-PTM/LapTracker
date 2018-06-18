import time
import math
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


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

        self.font_speed = ImageFont.truetype('/home/pi/pixelmix.ttf', 28)
        self.font_kmh = ImageFont.truetype('/home/pi/pixelmix.ttf', 8)
        self.font_parameter = ImageFont.truetype('/home/pi/pixelmix.ttf', 16)

        self.disp.begin(contrast=38)
        
        # Clear display
        self.disp.clear()
        self.disp.display()

        self.alert = '----'

        # Draw a white filled box to clear the image
        self.draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
    
    # Variables in use
    speed = 0 # 
    distance = 0 
    laptime = 0
    screen = 0  # flag that informs which screen to show (for example: distance, time, etc)
    signalbar = False # true if there is signal, false otherwise
    currentposition = 0 # tells you how much faster or slower are you compare to previous lap
    vmax = 0 # max recorded speed
    alertsque = [] # queue with alerts
    defaultalertTTL = 2 # default time for alert to print for
    alertTTL = defaultalertTTL 

    def printmenu(self):
        # km/h
        self.draw.text((62, 17), 'km/h', font=self.font_kmh)

        # left menu (rectangle)
        self.draw.line((13, 0, 13, 47), fill=0)
        self.draw.line((0, 0, 0, 47), fill=0)
        self.draw.line((0, 0, 13, 0), fill=0)
        self.draw.line((0, 47, 13, 47), fill=0)

        # left menu (?shelves?)
        self.draw.line((0, 12, 13, 12), fill=0)
        self.draw.line((0, 24, 13, 24), fill=0)
        self.draw.line((0, 36, 13, 36), fill=0)

	    # print letters in submenu
        self.draw.text((4, 2), 'S', font=self.font_kmh)
        self.draw.text((4, 14), 'T', font=self.font_kmh)
        self.draw.text((4, 26), 'L', font=self.font_kmh)
        self.draw.line((4, 39, 6, 44), fill=0)
        self.draw.line((8, 39, 6, 44), fill=0)

        if self.screen == 0:
            self.draw.rectangle((1, 1, 12, 11), outline=0, fill=255)
            self.draw.rectangle((1, 37, 12, 46), outline=255, fill=255)
            self.draw.text((4, 2), 'S', font=self.font_kmh)
            self.draw.line((4, 39, 6, 44), fill=0) #print V
            self.draw.line((8, 39, 6, 44), fill=0) #print V
        elif self.screen == 1:
            self.draw.rectangle((1, 1, 12, 11), outline=255, fill=255)
            self.draw.rectangle((1, 13, 12, 23), outline=0, fill=255)
            self.draw.text((4, 14), 'T', font=self.font_kmh)
            self.draw.text((4, 2), 'S', font=self.font_kmh)
        elif self.screen == 2:
            self.draw.rectangle((1, 13, 12, 23), outline=255, fill=255)
            self.draw.rectangle((1, 25, 12, 35), outline=0, fill=255)
            self.draw.text((4, 26), 'L', font=self.font_kmh)
            self.draw.text((4, 14), 'T', font=self.font_kmh)
        elif self.screen == 3:
            self.draw.rectangle((1, 25, 12, 35), outline=255, fill=255)
            self.draw.rectangle((1, 37, 12, 46), outline=0, fill=255)
            self.draw.line((4, 39, 6, 44), fill=0) #print V
            self.draw.line((8, 39, 6, 44), fill=0) #print V
            self.draw.text((4, 26), 'L', font=self.font_kmh)

    def printspeed(self):
        # Clear the speed
        self.draw.rectangle((17, 0, 61, 28), outline=255, fill=255)

        # Print the speed
        self.draw.text((17, -3), str(self.speed), font=self.font_speed)
        return

    def nextscreen(self):
        #Changes the flag of a screen after clicking the button
        self.screen += 1
        if self.screen == 4:
            self.screen = 0

    def printdistance(self):
        
        # Clear the display
        self.draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
        self.draw.text((70, 35), 'km', font=self.font_kmh)
        # Print the distance
        self.draw.text((17, 28), "{:0.2f}".format(self.distance), font=self.font_parameter)

    def printlaptime(self):
        # Clear the display
        self.draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
        # Print lap time
        self.draw.text((17, 28), str(self.laptime), font=self.font_parameter)

    def printlap(self):
        # Clear the display
        self.draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
        self.draw.text((70, 35), '', font=self.font_kmh)
		# Print currentposition
        if(self.currentposition > 0):
            self.draw.text((17, 28), str(str(self.currentposition)), font=self.font_parameter)
        else:
            self.draw.text((17, 28), str(str(self.currentposition)), font=self.font_parameter)

    def printvmax(self): 
        # Clear the display
        self.draw.rectangle((14, 26, 83, 47), outline=255, fill=255)

		# Printvmax
        self.draw.text((62, 35), 'km/h', font=self.font_kmh)
        self.draw.text((17, 28), str(self.vmax), font=self.font_parameter)
        
    def printsubmenu(self):
        if self.screen == 0:
            self.printdistance()
        elif self.screen == 1:
            self.printlaptime()
        elif self.screen == 2:
            self.printlap()
        else:
            self.printvmax()

    def printsignalbar(self): #prints gps signal
        if self.signalbar == True:
            self.draw.rectangle((62, 0, 69, 8), outline=255, fill=255)
            self.draw.rectangle((62, 4, 63, 8), outline=0, fill=0)
            self.draw.rectangle((65, 2, 66, 8), outline=0, fill=0)
            self.draw.rectangle((68, 0, 69, 8), outline=0, fill=0)
        elif self.signalbar == False:
            self.draw.rectangle((62, 0, 69, 8), outline=255, fill=255)
            self.draw.text((64, 1), 'X', font=self.font_kmh)

    def printcurrentposition(self): #prints information about current position
        if self.currentposition < 0:
            self.draw.rectangle((72, 0, 83, 15), outline=255, fill=255)
            #draw SPEEDUP symbol
            self.draw.rectangle((76, 4, 79, 15), outline=0, fill=0)
            self.draw.line((73, 4, 82, 4), fill=0)
            self.draw.line((74, 3, 81, 3), fill=0)
            self.draw.line((75, 2, 80, 2), fill=0)
            self.draw.line((76, 1, 79, 1), fill=0)
            self.draw.line((77, 0, 78, 0), fill=0)
        elif self.currentposition >= 0:
            self.draw.rectangle((72, 0, 83, 15), outline=255, fill=255)    
            #draw SLOWDWON symbol
            self.draw.rectangle((76, 0, 79, 10), outline=0, fill=0)
            self.draw.line((73, 11, 82, 11), fill=0)
            self.draw.line((74, 12, 81, 12), fill=0)
            self.draw.line((75, 13, 80, 13), fill=0)
            self.draw.line((76, 14, 79, 14), fill=0)
            self.draw.line((77, 15, 78, 15), fill=0)

    def show(self):
        alertsquelength = int(len(self.alertsque)) # the length of queue of alerts
        if alertsquelength>0: #if there are alerts
            if self.alertTTL > 0 and alertsquelength > 0:
                self.alertTTL = self.alertTTL - 1

            self.draw.rectangle((0, 0, 83, 47), outline=0, fill=255)
            self.draw.rectangle((3, 3, 80, 44), outline=0, fill=255)

            if alertsquelength == 1 and self.alertTTL < 1:
                self.draw.text((10, 20), str(self.alertsque[0]), font=self.font_kmh)
                self.alert = self.alertsque.pop(0)
                self.alertTTL = self.defaultalertTTL
            elif alertsquelength > 1 and self.alertTTL < 1:
                self.draw.text((10, 20), str(self.alertsque[0]), font=self.font_kmh)
                self.alert = self.alertsque.pop(0)
                self.alertTTL = self.defaultalertTTL
            elif alertsquelength > 0 and self.alertTTL > 0:
                self.draw.text((10, 20), str(self.alertsque[0]), font=self.font_kmh)

            self.disp.image(self.image)
            self.disp.display()

        else: #prints complete menu if no alerts
            self.draw.rectangle((0, 0, 83, 47), outline=255, fill=255)
            self.printmenu()
            self.printspeed()
            self.printsubmenu()
            self.printsignalbar()
            self.printcurrentposition()
            self.disp.image(self.image)
            self.disp.display()


																	    #
    # SETTERS for speed, distance, laptime, currentposition, alert       #
    # TOGGLE for signalbar												  #
    # TO SWITCH TO NEXT SCREEN USE <name of object>.nextscreen()               #
                                                                            #
    def setspeed(self, new):											    #		                         _     _       _      
        self.speed = new													#		                        | |   | |     (_)     
																			#		  _   _   ___    ___    | |_  | |__    _   ___ 
    def setdistance(self, new):												#		 | | | | / __|  / _ \   | __| | '_ \  | | / __|
        self.distance = new													#		 | |_| | \__ \ |  __/   | |_  | | | | | | \__ \
																			#		  \__,_| |___/  \___|    \__| |_| |_| |_| |___/
    def setlaptime(self, new):												#
        self.laptime = new													####	   ____    _   _   _       __     __
																			#		  / __ \  | \ | | | |      \ \   / /
    def setsignalbar(self, new):											#		 | |  | | |  \| | | |       \ \_/ / 
        self.signalbar = new									            #		 | |  | | | . ` | | |        \   /  
                                           									#		 | |__| | | |\  | | |____     | |   
                                             						    	#		  \____/  |_| \_| |______|    |_|								                    	
    def setcurrentposition(self, new):                                      #      
        self.currentposition = new                                         #     
                                                                          #
    def pushalert(self, newalert):	                                     #
        templist = [newalert]                                           #
        self.alertsque = self.alertsque + templist				       #
																   	  #
