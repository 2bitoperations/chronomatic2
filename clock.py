# grab the font:
# https://github.com/adafruit/Adafruit_CircuitPython_framebuf/raw/master/examples/font5x8.bine

import busio
import digitalio
import time
import board
import Matrix8xN

cs = digitalio.DigitalInOut(board.CE0)

spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
display = Matrix8xN.Matrix8xN(spi, cs, width=32, height=8)

display.clear_all()
display.brightness(1)

# framebuffer top left is 0,0!

while True:
    display.clear_all()
    display.framebuf.text(strg="Howdy!", xpos=0, ypos=0, bit_value=1)
    display.show()
    time.sleep(1)
    display.clear_all()
    display.framebuf.text(strg="Y'all", xpos=0, ypos=0, bit_value=1)
    display.show()
    time.sleep(1)
