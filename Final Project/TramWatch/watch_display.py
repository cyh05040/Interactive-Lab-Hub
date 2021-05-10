#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13d
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import paho.mqtt.client as mqtt
import uuid
import signal



topic = 'IDD/nani/trams/#'
topic1 = 'trams/1'
topic2 = 'trams/2'

class positions:
    def __init__(self):
        self.pos1 = 0
        self.pos2 = 0


pos = positions()

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)
def on_message(client, userdata, msg):
    # if a message is recieved on topic, print message
    if topic1 in msg.topic:
        pos.pos1 = int(msg.payload.decode('UTF-8'))
    if topic2 in msg.topic:
        pos.pos2 = int(msg.payload.decode('UTF-8'))

# this lets us exit gracefully (close the connection to the broker)
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)
    

# when sigint happens, do the handler callback function
signal.signal(signal.SIGINT, handler)

#Set output log level
logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13d Demo")
    
    epd = epd2in13d.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    
    client = mqtt.Client(str(uuid.uuid1()))
    client.tls_set()
    client.username_pw_set('idd', 'device@theFarm')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(
        'farlab.infosci.cornell.edu',
        port=8883)
    client.loop_start()

    # Drawing on the Horizontal image
    while True:

        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        i1 = 30 + int(pos.pos1*150/100.0)
        i2 = 30 + int(pos.pos2*150/100.0)
        # Track
        draw.line([(0,65),(30,50)], fill = 0,width = 1)
        draw.line([(30,50),(180,50)], fill = 0,width = 1)
        draw.line([(180,50),(220,65)], fill = 0,width = 1)

        # Tram 1
        draw.line([(i1 ,55),(i1,50)], fill = 0,width = 1)
        draw.rectangle((i1-7, 58, i1-4, 60), outline = 0)
        draw.rectangle((i1-2, 58, i1+1, 60), outline = 0)
        draw.rectangle((i1+3, 58, i1+6, 60), outline = 0)

        draw.ellipse((i1-10, 55, i1+10, 65), outline = 0)

        # Tram 2
        draw.line([(i2 ,55),(i2,50)], fill = 0,width = 1)
        draw.rectangle((i2-7, 58, i2-4, 60), outline = 0)
        draw.rectangle((i2-2, 58, i2+1, 60), outline = 0)
        draw.rectangle((i2+3, 58, i2+6, 60), outline = 0)

        draw.ellipse((i2-10, 55, i2+10, 65), outline = 0)

        # Sticker Figure
        draw.ellipse((5, 5, 15, 15), outline = 0)
        draw.line([(10,18),(13,21)], fill = 0,width = 1)
        draw.line([(10,18),(7,21)], fill = 0,width = 1)
        draw.line([(10,15),(10,25)], fill = 0,width = 1)
        draw.line([(10,25),(12,30)], fill = 0,width = 1)
        draw.line([(10,25),(8,30)], fill = 0,width = 1)

        # X ?
        draw.line([(20,10),(30,20)], fill = 0,width = 1)
        draw.line([(20,20),(30,10)], fill = 0,width = 1)
        draw.text((35, 2), '7', font = font24, fill = 0)

        # Sticker Figure
        draw.ellipse((119, 5, 129, 15), outline = 0)
        draw.line([(124,18),(127,21)], fill = 0,width = 1)
        draw.line([(124,18),(121,21)], fill = 0,width = 1)
        draw.line([(124,15),(124,25)], fill = 0,width = 1)
        draw.line([(124,25),(126,30)], fill = 0,width = 1)
        draw.line([(124,25),(122,30)], fill = 0,width = 1)

        # X ?
        draw.line([(135,10),(145,20)], fill = 0,width = 1)
        draw.line([(135,20),(145,10)], fill = 0,width = 1)
        draw.text((150, 2), '25', font = font24, fill = 0)


        draw.text((0, 80), 'NY', font = font24, fill = 0)
        draw.text((190, 80), 'RI', font = font24, fill = 0)

        epd.display(epd.getbuffer(Himage))
        time.sleep(1)



    # logging.info("3.read bmp file")
    # Himage = Image.open(os.path.join(picdir, '2in13d.bmp'))
    # epd.display(epd.getbuffer(Himage))
    # time.sleep(2)
    
    # logging.info("4.read bmp file on window")
    # Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    # bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    # Himage2.paste(bmp, (20,0))
    # epd.display(epd.getbuffer(Himage2))
    # time.sleep(2)
    
    # partial update
    logging.info("5.show time...")
    # epd.init()    
    # epd.Clear(0xFF)
    # time_image = Image.new('1', (epd.width, epd.height), 255)
    # time_draw = ImageDraw.Draw(time_image)
    # num = 0
    # while (True):
        # time_draw.rectangle((10, 10, 120, 50), fill = 255)
        # time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        # newimage = time_image.crop([10, 10, 120, 50])
        # time_image.paste(newimage, (10,10))  
        # epd.DisplayPartial(epd.getbuffer(time_image))
        # num = num + 1
        # if(num == 10):
            # break
    
    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13d.epdconfig.module_exit()
    exit()
