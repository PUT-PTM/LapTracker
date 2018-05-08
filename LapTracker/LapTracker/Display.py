import time
import math
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Initialize library.
disp.begin(contrast=50)

# Set fonts
font_speed = ImageFont.truetype('pixelmix.ttf', 28)
font_kmh = ImageFont.truetype('pixelmix.ttf', 8)
font_parameter = ImageFont.truetype('pixelmix.ttf', 16)

# Clear display
disp.clear()
disp.display()
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image
draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)

# Load an image, resize it, and convert to 1 bit color
# image = Image.open('name.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT)).convert('1')

# Variables
speed = 85
distance = 10.3
laptime = 430.0

screen = 0  # Flag that informs which screen to show (for example: distance, time, etc)
signalbar = False #True if there is signal, False otherwise
currentposition = False #False if you have to speed up, True if you are faster than before


# Display image.
disp.image(image)
disp.display()


def printmenu():
    # km/h
    draw.text((62, 17), 'km/h', font=font_kmh)

    # left menu (rectangle)
    draw.line((13, 0, 13, 47), fill=0)
    draw.line((0, 0, 0, 47), fill=0)
    draw.line((0, 0, 13, 0), fill=0)
    draw.line((0, 47, 13, 47), fill=0)

    # left menu (?shelves?)
    draw.line((0, 12, 13, 12), fill=0)
    draw.line((0, 24, 13, 24), fill=0)
    draw.line((0, 36, 13, 36), fill=0)
	
	#print letters in submenu
    draw.text((4, 2), 'S', font=font_kmh)
    draw.text((4, 14), 'T', font=font_kmh)
    draw.text((4, 26), 'L', font=font_kmh)
    draw.line((6, 39, 6, 44), fill=0)


def printspeed():
    global speed
    global image
    # Clear the speed
    draw.rectangle((17, 0, 61, 28), outline=255, fill=255)

    # Print the speed
    draw.text((17, -3), str(speed), font=font_speed)

    # Test of speed
    speed += 5
    if speed > 80:
        speed = 1
    # End of the test
    return

def nextscreen():
    #Changes the flag of a screen after clicking the button
    global screen
    screen += 1
    if screen == 4:
        screen = 0
	
	#Lines below print currently chosen submenu
    if screen == 0:
        draw.rectangle((1, 1, 12, 11), outline=0, fill=255)
        draw.rectangle((1, 37, 12, 46), outline=255, fill=255)
        draw.text((4, 2), 'S', font=font_kmh)
        draw.line((6, 39, 6, 44), fill=0)
    elif screen == 1:
        draw.rectangle((1, 1, 12, 11), outline=255, fill=255)
        draw.rectangle((1, 13, 12, 23), outline=0, fill=255)
        draw.text((4, 14), 'T', font=font_kmh)
        draw.text((4, 2), 'S', font=font_kmh)
    elif screen == 2:
        draw.rectangle((1, 13, 12, 23), outline=255, fill=255)
        draw.rectangle((1, 25, 12, 35), outline=0, fill=255)
        draw.text((4, 26), 'L', font=font_kmh)
        draw.text((4, 14), 'T', font=font_kmh)
    elif screen == 3:
        draw.rectangle((1, 25, 12, 35), outline=255, fill=255)
        draw.rectangle((1, 37, 12, 46), outline=0, fill=255)
        draw.line((6, 39, 6, 44), fill=0)
        draw.text((4, 26), 'L', font=font_kmh)


def printdistance():
	global distance
	global image
	
	distance+=0.25
	if distance > 99:
		distance -= 99
		
    # Clear the display
	draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
	draw.text((70, 35), 'km', font=font_kmh)
    # Print the distance
	draw.text((17, 28), str(distance), font=font_parameter)

def printlaptime():
	global laptime
	global image
		
    # Clear the display
	draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
	draw.text((75, 35), 's', font=font_kmh)
    # Print lap time
	draw.text((17, 28), str(laptime), font=font_parameter)
	
def something1():
	global image
		
    # Clear the display
	draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
	draw.text((70, 35), '', font=font_kmh)
    # Print sth
	draw.text((17, 28), str('sth :('), font=font_parameter)

def something2():
	global image
		
    # Clear the display
	draw.rectangle((14, 26, 83, 47), outline=255, fill=255)
	draw.text((70, 35), '', font=font_kmh)
    # Print sth
	draw.text((17, 28), str('sth :)'), font=font_parameter)

def printsubmenu():
	global screen    

	if screen == 0:
		printdistance()
	elif screen == 1:
		printlaptime()
	elif screen == 2:
		something1()
	else:
		something2()

def printsignalbar(): #prints gps signal
    global signalbar
    if signalbar == True:
        draw.rectangle((62, 0, 69, 8), outline=255, fill=255)
        draw.rectangle((62, 5, 63, 8), outline=0, fill=0)
        draw.rectangle((65, 2, 66, 8), outline=0, fill=0)
        draw.rectangle((68, 0, 69, 8), outline=0, fill=0)
    elif signalbar == False:
        draw.rectangle((62, 0, 69, 8), outline=255, fill=255)
        draw.text((64, 1), 'X', font=font_kmh)
    
    signalbar = not signalbar

def printcurrentposition(): #prints information about current position
    global currentposition
    if currentposition == False:
        draw.rectangle((72, 0, 83, 15), outline=255, fill=255)
        #draw SPEEDUP symbol
        draw.rectangle((76, 4, 79, 15), outline=0, fill=0)
        draw.line((73, 4, 82, 4), fill=0)
        draw.line((74, 3, 81, 3), fill=0)
        draw.line((75, 2, 80, 2), fill=0)
        draw.line((76, 1, 79, 1), fill=0)
        draw.line((77, 0, 78, 0), fill=0)
        

    elif currentposition == True:
        draw.rectangle((72, 0, 83, 15), outline=255, fill=255)    
        #draw SLOWDWON symbol
        draw.rectangle((76, 0, 79, 10), outline=0, fill=0)
        draw.line((73, 11, 82, 11), fill=0)
        draw.line((74, 12, 81, 12), fill=0)
        draw.line((75, 13, 80, 13), fill=0)
        draw.line((76, 14, 79, 14), fill=0)
        draw.line((77, 15, 78, 15), fill=0)
    
    currentposition = not currentposition




print('Press Ctrl-C to quit.')
printmenu()
while True:
	printspeed()
	printsubmenu()
	printsignalbar()
	printcurrentposition()
	disp.image(image)
	disp.display()
	nextscreen()
	time.sleep(1)