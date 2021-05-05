import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont

from time import strftime, sleep
import random

############### For touch sensors
import busio
import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)
############### For gesture sensors
# apds = adafruit_apds9960.apds9960.APDS9960(i2c)

# apds.enable_proximity = True
# apds.proximity_interrupt_threshold = (0, 175)
# apds.enable_proximity_interrupt = True

# apds.enable_gesture = True

############### For screen display

from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors

# The display uses a communication protocol called SPI.
# SPI will not be covered in depth in this course. 
# you can read more https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # the rate  the screen talks to the pi
# Create the ST7789 display:
disp = st7789.ST7789(
    board.SPI(),
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

font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
font_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 90)


# Pour beer and volume counts down
def pour_beer(number):
    if number is 5:
        for i in range(9999):
            draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
            draw.text((10, 10), 'Beer Remaining', font=font_small, fill='white')
            draw.text((10, 30), str(9999-i), font=font_big, fill='yellow')
            disp.image(image, rotation)
            time.sleep(0.05)  # Small delay to keep from spamming output messages.
    else:
        order_beer()
    
        


def order_beer():
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    draw.text((10, 10), 'Thank you for ordering:', font=font_small, fill='white')
    draw.text((10, 30), 'A New Box of', font=font_small, fill='white')
    draw.text((10, 50), 'Kirin!', font=font_big, fill='yellow')
    disp.image(image, rotation)
    time.sleep(5)  # Small delay to keep from spamming output messages.


def beer_logo():
    show_image('kirin-ichiban.png')


def show_image(filename):
    image = Image.open(filename)
    image = image_formatting(image)
    draw = ImageDraw.Draw(image)
    disp.image(image, rotation)


def image_formatting(image2):
    image2 = image2.convert('RGB')
    # Scale the image to the smaller screen dimension
    image2 = image2.resize((240, 135), Image.BICUBIC)
    return image2


    

   


# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# print("w", width) # w 240
# print("h", height) # h 135

up = 3
down = 0

while True:
    for i in range(12):
        if not mpr121[i].value:
            beer_logo()                
        else:
            print(f"Banana {i} touched!")
            pour_beer(i)





