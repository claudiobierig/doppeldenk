#!/usr/bin/env python
"""
Module containing Svg class and helper functions
"""
import math
from lxml import etree
import lxml


def json_to_style(json):
    """
    convert a json to a string formated as style argument
    { a : "b", c : "d" } -> "a:b;c:d;"
    """
    style_argument = ""
    for attribute, value in json.items():
        style_argument = style_argument + attribute + ":" + value + ";"

    return style_argument


class Svg(object):
    """
    Class managing SVG elements via lxml.etree
    """
    def __init__(self, root=None, width=0, height=0, id_name="svg_element"):
        if root is None:
            self.root = lxml.etree.Element("svg",
                                           {"width": str(width),
                                            "height": str(height),
                                            "id": id_name
                                           })
        else:
            self.root = root

    def create_subgroup(self, group_id, class_name=None):
        """
        create a subgroup in root and return it
        """
        arguments = {'id': str(group_id)}
        if class_name is not None:
            arguments['class'] = str(class_name)

        group = etree.SubElement(self.root, 'g', arguments)
        return Svg(group)

    def create_ellipse(
            self,
            radius,
            center,
            stroke_colour,
            id_name,
            fill=None,
            stroke_width="1",
            stroke_opacity="0.5",
            opacity="1"):
        """
        Create an ellipse in root and return it
        """
        (radius_x, radius_y) = radius
        (center_x, center_y) = center
        style = {
            'stroke': stroke_colour,
            'stroke-width': stroke_width,
            'stroke-opacity': stroke_opacity
        }
        if fill:
            style['fill'] = str(fill)
            style['opacity'] = str(opacity)

        ell_attribs = {
            'style': json_to_style(style),
            'cx': str(center_x),
            'cy': str(center_y),
            'rx': str(radius_x),
            'ry': str(radius_y),
            'id': str(id_name)
        }

        ellipse = etree.SubElement(self.root, 'ellipse', ell_attribs)
        return Svg(ellipse)

    def create_hex(
            self,
            id_name,
            center,
            coordinates,
            hex_size,
            fill_colour,
            class_name,
            fill_opacity="0.5",
            stroke_colour='#FFFFFF',
            stroke_width="1",
            onclick="clickHex(this)",
            onmouseover="mouseOverHex(this)",
            onmouseout="mouseOutHex(this)"):
        """
        Create a hex in root and return it
        """
        (center_x, center_y) = center
        (coord_q, coord_r) = coordinates
        hex_width = float(2 * hex_size)
        hex_height = math.sqrt(3) * hex_size

        points = [
            [center_x - hex_width / 4, center_y - hex_height / 2],
            [center_x + hex_width / 4, center_y - hex_height / 2],
            [center_x + hex_width / 2, center_y],
            [center_x + hex_width / 4, center_y + hex_height / 2],
            [center_x - hex_width / 4, center_y + hex_height / 2],
            [center_x - hex_width / 2, center_y]
        ]
        str_points = ""
        for point in points:
            str_points = str_points + str(point[0]) + "," + str(point[1]) + " "

        style = {
            'stroke': stroke_colour,
            'stroke-width': str(stroke_width),
            'fill': fill_colour,
            'fill-opacity': str(fill_opacity)
        }
        ell_attribs = {
            'style': json_to_style(style),
            'points': str_points,
            'id': str(id_name),
            'coord_q': str(coord_q),
            'coord_r': str(coord_r),
            'onclick': onclick,
            'onmouseover': onmouseover,
            'onmouseout': onmouseout,
            'class': class_name
        }

        hex_element = etree.SubElement(self.root, 'polygon', ell_attribs)
        return Svg(hex_element)

    def create_text(
            self,
            position,
            content,
            font_size="8pt",
            font_colour="#000000",
            text_align="center",
            text_anchor="middle"):
        """
        Create a text in root and return it
        """
        (position_x, position_y) = position
        style = {
            'text-align': text_align,
            'text_anchor': text_anchor,
            'font_size': font_size
        }
        attributes = {
            'style': json_to_style(style),
            'x': str(position_x),
            'y': str(position_y),
            'fill': font_colour,
            'id': content
        }

        text = etree.SubElement(self.root, 'text', attributes)
        text.text = content
        return Svg(text)

    def create_rectangle(
            self,
            position,
            size,
            id_name,
            fill_colour=None,
            stroke_colour=None,
            stroke_width=None,
            fill_opacity=None,
            additional_arguments=None):
        """
        Create a rectangle in root and return it
        """
        (position_x, position_y) = position
        (size_width, size_height) = size
        if additional_arguments is None:
            additional_arguments = {}

        style = {}

        if fill_colour:
            style['fill'] = fill_colour

        if stroke_colour:
            style['stroke'] = stroke_colour

        if stroke_width:
            style['stroke-width'] = str(stroke_width)

        if fill_opacity:
            style['fill-opacity'] = str(fill_opacity)

        arguments = {
            'style': json_to_style(style),
            'id': id_name,
            'width': str(size_width),
            'height': str(size_height),
            'x': str(position_x),
            'y': str(position_y),
        }

        for attribute, value in additional_arguments.items():
            arguments[attribute] = value

        rect = etree.SubElement(self.root, 'rect', arguments)
        return Svg(rect)

    def create_circle(self, center, radius, id_name,
                      fill_colour=None, additional_arguments=None):
        """
        Create a circle in root and return it
        """
        (center_x, center_y) = center
        if additional_arguments is None:
            additional_arguments = {}

        arguments = {
            'id': id_name,
            'cx': str(center_x),
            'cy': str(center_y),
            'r': str(radius)
        }
        if fill_colour is not None:
            arguments["style"] = "fill:" + fill_colour

        for attribute, value in additional_arguments.items():
            arguments[attribute] = value

        circle = etree.SubElement(self.root, 'circle', arguments)
        return Svg(circle)

    def add_posibility_for_disc_3d(self):
        """
        Create a symbol, which represents a 3d disc in root and return it
        """
        symbol = Svg(etree.SubElement(self.root,
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

    def create_3d_disc(self, id_name, position,
                       fill_colour, additional_arguments=None):
        """
        Create a 3d disc in root and return it.
        This will only work when add_posibility_for_disc_3d was called before.
        """
        (position_x, position_y) = position
        if additional_arguments is None:
            additional_arguments = {}

        style = {
            'fill': fill_colour
        }
        arguments = {
            'href': '#disc_3d',
            'id': id_name,
            'x': str(position_x),
            'y': str(position_y),
            'style': json_to_style(style)
        }

        for attribute, value in additional_arguments.items():
            arguments[attribute] = value

        disc = etree.SubElement(self.root, 'use', arguments)
        return Svg(disc)

    def create_image(self, parent, image_name):
        """
        Create an image in root and return it.
        """
        image = etree.SubElement(parent, 'image', {'href': image_name})
        return Svg(image)


def main():
    """
    no main implemented
    """
    print "no main implemented"


if __name__ == '__main__':
    main()
