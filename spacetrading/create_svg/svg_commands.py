#!/usr/bin/env python
"""
Module containing Svg class and helper functions
"""
import math
from lxml import etree


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
            self.root = etree.Element("svg",
                                      {"width": str(width),
                                       "height": str(height),
                                       "id": id_name
                                       })
        else:
            self.root = root

    def create_subgroup(
            self,
            group_id,
            class_name=None,
            additional_arguments=None):
        """
        create a subgroup in root and return it
        """
        arguments = {'id': str(group_id)}
        if class_name is not None:
            arguments['class'] = str(class_name)

        if additional_arguments is not None:
            arguments.update(additional_arguments)
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
            'stroke-width': str(stroke_width),
            'stroke-opacity': str(stroke_opacity),
        }

        if fill is not None:
            style['fill'] = fill
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
            enableOnClick=False,
            onclick="clickHex(this)",
            stroke_opacity="1"):
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
            'stroke-opacity': str(stroke_opacity),
            'fill': fill_colour,
            'fill-opacity': str(fill_opacity)
        }
        ell_attribs = {
            'style': json_to_style(style),
            'points': str_points,
            'id': str(id_name),
            'coord_q': str(coord_q),
            'coord_r': str(coord_r),
            'class': class_name
        }
        if enableOnClick:
            ell_attribs['onclick'] = onclick

        hex_element = etree.SubElement(self.root, 'polygon', ell_attribs)
        return Svg(hex_element)

    def create_text(
            self,
            id_name,
            position,
            content,
            font_size=8,
            font_colour="#000000",
            text_align="center",
            text_anchor="middle"):
        """
        Create a text in root and return it
        """
        (position_x, position_y) = position
        style = {
            'text-align': text_align,
            'text-anchor': text_anchor,
            'font-size': str(font_size) + "pt"
        }
        attributes = {
            'style': json_to_style(style),
            'x': str(position_x),
            'y': str(position_y),
            'fill': font_colour,
            'id': id_name
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

    def create_line(self, position_start, position_end,
                    stroke_colour="#000000",
                    stroke_width="1"):
        """
        create a line in root and return it
        """
        (start_x, start_y) = position_start
        (end_x, end_y) = position_end
        style = {
            'stroke': stroke_colour,
            'stroke-width': str(stroke_width)
        }
        arguments = {
            'x1': str(start_x),
            'x2': str(end_x),
            'y1': str(start_y),
            'y2': str(end_y),
            'style': json_to_style(style)
        }
        line = etree.SubElement(self.root, 'line', arguments)
        return Svg(line)

    def create_path(self, commands, stroke_colour=None, fill_colour=None,
                    id_name=None, additional_arguments=None):
        """
        create a path in root and return it
        """
        arguments = {
            'd': commands
        }

        if stroke_colour is not None:
            arguments["stroke"] = stroke_colour

        if fill_colour is not None:
            arguments["fill"] = fill_colour

        if id_name is not None:
            arguments['id'] = id_name

        if additional_arguments is not None:
            arguments.update(additional_arguments)

        path = etree.SubElement(self.root, 'path', arguments)
        return Svg(path)

    def create_polygon(self, points, fill_colour=None, stroke_colour=None):
        """
        create a polygon in root and return it
        """
        arguments = {
            'points': points
        }
        style = {}
        if fill_colour is not None:
            style['fill'] = fill_colour

        if stroke_colour is not None:
            style['stroke'] = stroke_colour

        arguments['style'] = json_to_style(style)
        polygon = etree.SubElement(self.root, 'polygon', arguments)
        return Svg(polygon)

    def use_symbol(self, symbol_name, id_name, position=None,
                   fill_colour=None, additional_arguments=None):
        """use a symbol which had to be defined earlier

        Arguments:
            symbol_name {string} -- name of the symbol
            id_name {string} -- id
            position {(int, int)} -- (x, y) (default: {None})

        Keyword Arguments:
            fill_colour {string} -- colour (default: {None})
            additional_arguments {json} -- any additional arguments (default: {None})
        """
        if additional_arguments is None:
            additional_arguments = {}

        arguments = {
            'href': '#' + symbol_name,
            'id': id_name
        }

        if position is not None:
            (position_x, position_y) = position
            arguments['x'] = str(position_x)
            arguments['y'] = str(position_y)
        if fill_colour is not None:
            arguments["style"] = json_to_style({'fill': fill_colour})

        for attribute, value in additional_arguments.items():
            arguments[attribute] = value

        symbol = etree.SubElement(self.root, 'use', arguments)
        return Svg(symbol)

    def create_image(self, image_name, width, height, x_pos, y_pos):
        """
        Create an image in root and return it.
        """
        image = etree.SubElement(self.root, 'image', {'href': image_name, 'width': width, 'height': height, 'x': x_pos, 'y': y_pos})
        image.text = " "
        return Svg(image)

    def create_scoring_track(self, size_box, subgroup_name, x_elements, y_elements, grey_element, fill_colour="#FFFFFF", font_size=8, additional_arguments=None):
        """
        create the whole scoring track
        """
        if additional_arguments is None:
            additional_arguments = {}
        layer = self.create_subgroup(subgroup_name)
        for i in range(0, x_elements + 1):
            layer.draw_scoring_box(
                (i*size_box, 0),
                (size_box, size_box),
                "{}_{}".format(subgroup_name, i),
                i,
                grey_element,
                fill_colour,
                font_size,
                additional_arguments
            )
        for i in range(x_elements, x_elements + y_elements + 1):
            layer.draw_scoring_box(
                (x_elements*size_box, (i - x_elements)*size_box),
                (size_box, size_box),
                "{}_{}".format(subgroup_name, i),
                i,
                grey_element,
                fill_colour,
                font_size,
                additional_arguments
            )
        for i in range(x_elements + y_elements, 2*x_elements + y_elements + 1):
            layer.draw_scoring_box(
                ((2*x_elements + y_elements - i)*size_box, y_elements*size_box),
                (size_box, size_box),
                "{}_{}".format(subgroup_name, i),
                i,
                grey_element,
                fill_colour,
                font_size,
                additional_arguments
            )
        for i in range(2*x_elements + y_elements, 2*x_elements + 2*y_elements):
            layer.draw_scoring_box(
                (0, (2*x_elements + 2*y_elements - i)*size_box),
                (size_box, size_box),
                "{}_{}".format(subgroup_name, i),
                i,
                grey_element,
                fill_colour,
                font_size,
                additional_arguments
            )
    
    def draw_scoring_box(self, position, size, id_name, number, grey_element, fill_colour="#FFFFFF", font_size=8, additional_arguments=None):
        """
        draw one box of the scoring track
        """
        if additional_arguments is None:
            additional_arguments = {}
        additional_arguments["value"] = str(number)

        (position_x, position_y) = position
        (width, height) = size

        self.create_rectangle((position_x, position_y), (width, height),
                                id_name, fill_colour=fill_colour,
                                stroke_colour="#000000",
                                stroke_width=1,
                                fill_opacity=1,
                                additional_arguments=additional_arguments)
        if number % grey_element == 0:
            self.create_rectangle(
                [position_x, position_y],
                size,
                "{}_transperent".format(id_name),
                fill_colour="black",
                fill_opacity="0.4"
            )
        self.create_text(
            id_name,
            (position_x + width / 2, position_y + height / 2 + font_size / 2),
            str(number),
            font_size=font_size
        )

    def get_string(self):
        """
        return root element converted to string
        """
        return etree.tostring(self.root, pretty_print=True).decode('utf-8')

    def __str__(self):
        return self.get_string()

def get_position(size, x_elements, y_elements, points, stack_position):
    """
    given the points and the number of markers below in the stack
    return the position where to print the marker
    """
    HEIGHT_DISC = 4
    POSITION_LOWEST_DISC = 15
    space = points % (2*(x_elements+y_elements))
    if 0 <= space <= x_elements:
        x_pos = space * size
        y_pos = POSITION_LOWEST_DISC
    elif x_elements < space <= x_elements + y_elements:
        x_pos = x_elements * size
        y_pos = POSITION_LOWEST_DISC + (space - x_elements) * size
    elif x_elements + y_elements < space <= 2*x_elements + y_elements:
        x_pos = (2*x_elements + y_elements - space) * size
        y_pos = POSITION_LOWEST_DISC + y_elements*size
    elif 2*x_elements + y_elements < space < 2*x_elements + 2*y_elements:
        x_pos = 0
        y_pos = POSITION_LOWEST_DISC + (2*x_elements + 2*y_elements - space) * size
    return [x_pos, y_pos - 4*stack_position]


def main():
    """
    no main implemented
    """
    print("no main implemented")


if __name__ == '__main__':
    main()
