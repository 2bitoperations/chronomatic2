from micropython import const
import max7219

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MAX7219.git"

_DECODEMODE = const(9)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)
_INTENSITY = const(10)


class Matrix8xN(max7219.MAX7219):
    """
    Driver for a 8x8 LED matrix based on the MAX7219 chip.
    :param object spi: an spi busio or spi bitbangio object
    :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
    """

    def __init__(self, spi, cs, width, height):
        super().__init__(width, height, spi, cs)

    def init_display(self):
        for cmd, data in (
                (_SHUTDOWN, 0),
                (_DISPLAYTEST, 0),
                (_SCANLIMIT, 7),
                (_DECODEMODE, 0),
                (_SHUTDOWN, 1),
        ):
            self.write_cmd_to_all(cmd, data)

        self.fill(0)
        self.show()

    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self.write_cmd_to_all(_INTENSITY, value)

    def text(self, strg, xpos, ypos, bit_value=1):
        """
        Draw text in the 8x8 matrix.
        :param int xpos: x position of LED in matrix
        :param int ypos: y position of LED in matrix
        :param string strg: string to place in to display
        :param bit_value: > 1 sets the text, otherwise resets
        """
        self.framebuf.text(strg, xpos, ypos, bit_value)

    def clear_all(self):
        """
        Clears all matrix leds.
        """
        self.fill(0)