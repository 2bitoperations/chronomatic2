# grab the font:
# https://github.com/adafruit/Adafruit_CircuitPython_framebuf/raw/master/examples/font5x8.bine

import busio
import digitalio
import time
import board
import Matrix8xN

cs = digitalio.DigitalInOut(board.CE0)

spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
display = Matrix8xN.Matrix8xN(spi, cs, width=8, height=32)

display.clear_all()
display.brightness(3)

while True:

    for i in range(0, 7):
        display.pixel(i, i, bit_value=1)
        display.pixel(i+8, 7-i, bit_value=1)
    display.show()

    time.sleep(1.0)
