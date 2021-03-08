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
font_one = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
font_two = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)
font_three = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
font_four = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)


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
    current_date = datetime.datetime.now().strftime("%m/%d/%Y")
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    hour = int(current[-8:-6])
    sec = int(current[-1:])
    sunset_time = 20

    # if buttonA.value and buttonB.value:
    #     backlight.value = False  # turn off backlight
    # else:
    backlight.value = True  # turn on backlight
    if (sec % 2 == 0):
        color_one = 'blue'
        color_two = 'orange'

    else:
        color_one = 'orange'
        color_two  = 'blue'
    draw.text((92, 50), current_date, font=font_two, fill=color_one)
    draw.text((80, 80), current_time, font=font_three, fill=color_two)

    if buttonB.value and not buttonA.value:  # just button A pressed
        draw.text((10, 10), 'You are in New York City', font=font_one, fill='white')
        draw.line((20, 130, 50, 130), fill='white')
        draw.line((20, 60, 20, 130), fill='white')
        draw.line((50, 60, 50, 130), fill='white')
        draw.line((20, 60, 50, 60), fill='white')
        draw.line((20, 60, 25, 55), fill='white')
        draw.line((50, 60, 45, 55), fill='white')
        draw.line((25, 55, 45, 55), fill='white')
        draw.line((30, 50, 40, 50), fill='white')
        draw.line((30, 50, 30, 55), fill='white')
        draw.line((40, 50, 40, 55), fill='white')
        draw.line((33, 45, 37, 45), fill='white')
        draw.line((33, 45, 37, 45), fill='white')
        draw.line((33, 45, 33, 50), fill='white')
        draw.line((37, 45, 37, 50), fill='white')
        draw.line((35, 35, 35, 45), fill='white')









        # draw.line((x+1, y+5, x+11, y+5), fill='white')
        # draw.line((x+11, y+5, x+2, y+11), fill='white')
        # draw.line((x+1, y+5, x+10, y+11), fill='white')
    

    if buttonA.value and not buttonB.value:  # just button B pressed
        if hour >= sunset_time:
            draw.text((20, 100), '35℉', font=font_one, fill='white')
            draw.text((20, 10), "( ͡❛ ͜ʖ ͡❛)", font=font_three, fill='orange')
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
            draw.text((20, 100), '35℉', font=font_one, fill='white')
            draw.ellipse((20, 20, 80, 80), fill = 'orange', outline ='orange')
            num_cloud = 0
            while num_cloud < hour:
                x = random.randint(0, 240) 
                y = random.randint(0, 135) 
                draw.text((x, y), '☁', font=font_one, fill='grey')
                num_cloud+=1
            

            



    # Display image.
    disp.image(image, rotation)
    time.sleep(0.3)