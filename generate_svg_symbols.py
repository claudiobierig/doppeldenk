#!/usr/bin/env python
"""
generate svg symbols
"""
import math
from lxml import etree

from svg_commands import Svg
from svg_commands import json_to_style


def add_posibility_for_disc_3d(svg):
    """
    Create a symbol, which represents a 3d disc in root and return it
    """
    symbol = Svg(etree.SubElement(svg.root,
                                  'symbol',
                                  {'id': 'disc_3d',
                                   'view_box': '0 0 30 15'
                                  }))
    symbol.create_ellipse((12, 4), (15, 9), "#000000",
                          "bottom", stroke_opacity="1")
    symbol.create_rectangle((3, 5), (24, 4), "middle")
    symbol.create_ellipse((12, 4), (15, 5), "#000000",
                          "top", stroke_opacity="1")
    linestyle = {
        'stroke': '#000000',
        'stroke-width': '1',
    }
    etree.SubElement(symbol.root, 'line',
                     {
                         'x1': "3",
                         'x2': "3",
                         'y1': "5",
                         'y2': "9",
                         'style': json_to_style(linestyle),
                     }
                    )
    etree.SubElement(symbol.root, 'line',
                     {
                         'x1': "27",
                         'x2': "27",
                         'y1': "5",
                         'y2': "9",
                         'style': json_to_style(linestyle),
                     })
    return symbol


def add_posibility_for_wheel(
        self,
        size,
        radius,
        colour_1,
        colour_2,
        values_1,
        values_2):
    """
    Create a symbol, which represents the foreground of the resource wheel
    <path d="M160,100 A1,1 0 0,1 160,220" stroke="#FFFFFF" fill="#FFFFFF" />
    <polygon points="160,-10 160,330 180,160" style="fill:#FFFFFF" />
    <path d="M160,100 A1,1 0 0,0 160,220" stroke="#000000" fill="#000000" />
    <polygon points="160,-10 160,330 140,160" style="fill:#000000" />
    """
    symbol = Svg(etree.SubElement(self.root,
                                  'symbol',
                                  {'id': 'foreground_symbol',
                                   'view_box': '0 0' + str(size) + ' ' + str(size)
                                  }))
    symbol.create_path("M{},{} A1,1 0 0,1 {},{}".format(size / 2,
                                                        size / 2 - radius,
                                                        size / 2,
                                                        size / 2 + radius),
                       colour_1, colour_1)
    symbol.create_polygon("{},{} {},{} {},{}".format(size / 2, -10,
                                                     size / 2, size + 10,
                                                     size / 2 + 20, size / 2),
                          colour_1)
    symbol.create_path("M{},{} A1,1 0 0,0 {},{}".format(size / 2,
                                                        size / 2 - radius,
                                                        size / 2,
                                                        size / 2 + radius),
                       colour_2, colour_2)
    symbol.create_polygon("{},{} {},{} {},{}".format(size / 2, -10,
                                                     size / 2, size + 10,
                                                     size / 2 - 20, size / 2),
                          colour_2)

    number_of_segments = len(values_1) + len(values_2)
    degrees = range(0, number_of_segments)
    degrees[:] = [2 * x * math.pi / number_of_segments for x in degrees]
    positions = [(radius * math.cos(x) + size / 2,
                  radius * math.sin(x) + size / 2)
                 for x in degrees]
    for position in positions:
        symbol.create_line([size / 2, size / 2], position)

    font_size = 8
    padding_numbers = 10
    radius_numbers = radius - padding_numbers
    number_of_segments_1 = len(values_1)
    degrees_1 = range(0, number_of_segments_1)
    degrees_1[:] = [- math.pi / 2 + (2 * x + 1) * math.pi / number_of_segments
                    for x in degrees_1]
    position_numbers_1 = [
        (radius_numbers * math.cos(x) + size / 2,
         radius_numbers * math.sin(x) + size / 2 + font_size / 2)
        for x in degrees_1
    ]
    for index, position in enumerate(position_numbers_1):
        symbol.create_text(position, str(values_1[index]),
                           font_size=font_size, font_colour=colour_2)

    number_of_segments_2 = len(values_2)
    degrees_2 = list(reversed(range(0, number_of_segments_2)))
    degrees_2[:] = [math.pi / 2 + (2 * x + 1) * math.pi / number_of_segments
                    for x in degrees_2]

    print degrees_1
    print degrees_2
    position_numbers_2 = [
        (radius_numbers * math.cos(x) + size / 2,
         radius_numbers * math.sin(x) + size / 2 + font_size / 2)
        for x in degrees_2
    ]

    for index, position in enumerate(position_numbers_2):
        symbol.create_text(position, str(values_2[index]),
                           font_size=font_size, font_colour=colour_1)


def main():
    """
    no main implemented
    """
    print "no main implemented"


if __name__ == '__main__':
    main()
