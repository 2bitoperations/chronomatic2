# grab the font:
# https://github.com/adafruit/Adafruit_CircuitPython_framebuf/raw/master/examples/font5x8.bine
# may need to manually install displayio:
# git clone https://github.com/2bitoperations/Adafruit_Blinka_Displayio.git
# cd Adafruit_Blinka_Displayio
# sudo pip3 install .
#
# ... and install:
# sudo apt install libopenjp2-7-dev libtiff5-dev libatlas-base-dev
from datetime import datetime
from os import truncate

import busio
import digitalio
import time
import board
import Matrix8xN
import logging
import requests
import sys
from adafruit_bitmap_font import bitmap_font

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
rootLogger.addHandler(ch)


def draw_font(string, font, framebuffer, x=0, y=0):
    _, height, _, dy = font.get_bounding_box()
    current_x_offset = x
    for c in string:
        glyph = font.get_glyph(ord(c))
        if not glyph:
            continue

        h_offset = height - glyph.height
        for hpos in range(glyph.height):
            for x_in_glyph in range(glyph.width):
                value = glyph.bitmap[(x_in_glyph, hpos)]
                framebuffer.pixel(x=current_x_offset + x_in_glyph, y=y + hpos + h_offset - glyph.dy, color=value)

        current_x_offset = current_x_offset + glyph.width + 1


cs = digitalio.DigitalInOut(board.CE0)

spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
display = Matrix8xN.Matrix8xN(spi, cs, width=32, height=8)

font = bitmap_font.load_font(filename="tom-thumb.bdf")

display.clear_all()
display.brightness(1)

# framebuffer top left is 0,0!

temp = None
while True:
    now = datetime.now()
    if now.second % 2 == 0:
        sep = ":"
    else:
        sep = " "

    if (not temp) or now.second == 0:
        try:
            r = requests.get('http://192.168.5.1:8088/wx/current')
            currWx = r.json()
            bed_temp = currWx['bed']['temp']
            temp = "{temp:2.0f}c".format(temp=bed_temp)
        except Exception as e:
            rootLogger.exception(currWx)
            temp = " "

    display.clear_all()
    time_str = now.strftime("%H{sep}%M".format(sep=sep))
    draw_font(time_str, font, display.framebuf)
    draw_font(temp, font, display.framebuf, x=21)
    display.framebuf.line(x_0=0, y_0=7, x_1=int((now.second / 60) * 31.0), y_1=7, color=1)
    display.show()
    time.sleep((1000000-now.microsecond)/1000000.0)
