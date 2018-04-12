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
font_speed = ImageFont.truetype('FreePixel.ttf', 28)
font_kmh = ImageFont.truetype('FreePixel.ttf', 8)
font_parameter = ImageFont.truetype('FreePixel.ttf', 16)

# Clear display.
disp.clear()
disp.display()
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image.
draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)

# Load an image, resize it, and convert to 1 bit color.
# image = Image.open('name.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT)).convert('1')

# Variables
speed = 85
distance = 10.3
laptime = 430.0

screen = 0  # Flag that informs which screen to show (for example: distance, time, etc)

# Display image.
disp.image(image)
disp.display()


def printmenu():
    # km/h
    draw.text((62, 17), 'km/h', font=font_kmh)

    # left menu (rectangle)
    draw.line((13, 0, 13, 47), fill=0)
    draw.line((0, 0, 0, 48), fill=0)
    draw.line((0, 0, 13, 0), fill=0)
    draw.line((0, 47, 13, 47), fill=0)

    # left menu (?shelves?)
    draw.line((0, 12, 13, 12), fill=0)
    draw.line((0, 24, 13, 24), fill=0)
    draw.line((0, 36, 13, 36), fill=0)

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
    return

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

print('Press Ctrl-C to quit.')
printmenu()
while True:
	printspeed()
	printsubmenu()
	disp.image(image)
	disp.display()
	nextscreen()
	time.sleep(1)