from adafruit_bitmap_font import bitmap_font


def draw_font(string, font):
    _, height, _, dy = font.get_bounding_box()
    current_x_offset = 0
    for c in string:
        glyph = font.get_glyph(ord(c))
        if not glyph:
            continue

        print("\n{char}=width{width} height{height} shift_x{shift_x} shift_y{shift_y} dx{dx} dy{dy}".format(
            char=c,
            width=glyph.width,
            height=glyph.height,
            shift_x=glyph.shift_x,
            shift_y=glyph.shift_y,
            dx=glyph.dx,
            dy=glyph.dy
        ))
        for hpos in range(glyph.height):
            for x_in_glyph in range(glyph.width):
                value = glyph.bitmap[(x_in_glyph, hpos)]
                print("{x}x{y}={v}".format(x=x_in_glyph, y=hpos, v=value))


font = bitmap_font.load_font(filename="tom-thumb.bdf")

draw_font(string="Howdy, Y'all!", font=font)
