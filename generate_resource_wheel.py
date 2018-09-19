#!/usr/bin/env python
"""
generate the resource wheel
"""

import math
from svg_commands import Svg
import generate_svg_symbols
import gamesettings

WIDTH = 320
HEIGHT = 320

assert WIDTH == HEIGHT

def draw_background(svg):
    """
    draw background of the wheel
    """
    layer = svg.create_subgroup("wheel_background")
    for index, planet in enumerate(reversed(gamesettings.PLANETS)):
        layer.create_circle((WIDTH/2, HEIGHT/2),
                            (8-index)*20,
                            planet.name + "_wheel_background",
                            fill_colour=planet.colour)

    number_of_segments = len(gamesettings.RESOURCE_BUY_PRICES)
    degrees_start = range(0, number_of_segments)
    degrees_end = range(number_of_segments, 2*number_of_segments)
    degrees_start[:] = [x * math.pi / number_of_segments for x in degrees_start]
    degrees_end[:] = [x * math.pi / number_of_segments for x in degrees_end]
    positions_start = [
        (WIDTH/2 *
         math.cos(x) +
         WIDTH/2,
         WIDTH/2 *
         math.sin(x) +
         WIDTH/2) for x in degrees_start]
    positions_end = [
        (WIDTH/2 *
         math.cos(x) +
         WIDTH/2,
         WIDTH/2 *
         math.sin(x) +
         WIDTH/2) for x in degrees_end]

    for index in range(0, number_of_segments):
        layer.create_line((positions_start[index][0],
                           positions_start[index][1]),
                          (positions_end[index][0],
                           positions_end[index][1]),
                          stroke_width=2)

def draw_foreground(svg):
    """
    draw the foreground of the wheel, i.e. the part that spins
    """
    layer = svg.create_subgroup("wheel_foreground")
    layer.use_symbol("foreground_symbol", "use_foreground", [0, 0])

def main():
    """
    draw the resource wheel
    """
    svg = Svg(width=str(WIDTH), height=str(HEIGHT), id_name="resource_wheel")
    generate_svg_symbols.add_posibility_for_wheel(svg, WIDTH, 60, "#BBBBBB", "#333333",
                                                  gamesettings.RESOURCE_BUY_PRICES,
                                                  gamesettings.RESOURCE_SELL_PRICES)
    draw_background(svg)
    draw_foreground(svg)
    svg_string = svg.get_string()
    print svg_string
    with open("wheel.svg", "w") as out_file:
        out_file.write(svg_string)


if __name__ == '__main__':
    main()
