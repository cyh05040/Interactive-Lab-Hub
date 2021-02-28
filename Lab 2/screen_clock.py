import time
import datetime
import subprocess
import digitalio
import board
import random
from random import randint
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep



# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


    

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 

    current = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    hour = int(current[-8:-6])
    sec = int(current[-1:])
    sunset_time = 18

    if buttonA.value and buttonB.value:
        backlight.value = False  # turn off backlight
    else:
        backlight.value = True  # turn on backlight
    
    if buttonB.value and not buttonA.value:  # just button A pressed
        if (sec % 2 == 0):
            color = 'blue'
        else:
            color  = 'orange'
        draw.text((30, 50), current, font=font, fill=color)


    if buttonA.value and not buttonB.value:  # just button B pressed
        if hour >= sunset_time:
            num_star = 0
            while num_star < hour:
                x = random.randint(0, 240) 
                y = random.randint(0, 135) 
                draw.line((x+6, y+2, x+2, y+11), fill='yellow')
                draw.line((x+6, y+2, x+10, y+11), fill='yellow')
                draw.line((x+1, y+5, x+11, y+5), fill='yellow')
                draw.line((x+11, y+5, x+2, y+11), fill='yellow')
                draw.line((x+1, y+5, x+10, y+11), fill='yellow')
                num_star+=1
        else:
            draw.ellipse((30, 30, 100, 100), fill = 'yellow', outline ='orange')



    # Display image.
    disp.image(image, rotation)
    time.sleep(0.3)