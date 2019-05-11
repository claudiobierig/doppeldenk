#!/usr/bin/env python
"""
generate the main gameboard
"""
import math
import subprocess
from spacetrading.create_svg.svg_commands import Svg

HEX_SIZE = 37

WIDTH = 1200
HEIGHT = 800

def get_hex_coordinates(position, hex_size):
    """
    convert position to hex coordinate
    """
    (position_x, position_y) = (
        position[0] - WIDTH / 2, position[1] - HEIGHT / 2)
    coord_q = (2. / 3 * position_x) / hex_size
    coord_r = (-1. / 3 * position_x + math.sqrt(3) / 3 * position_y) / hex_size
    coord_s = -(coord_q + coord_r)

    rounded_q = round(coord_q)
    rounded_r = round(coord_r)
    rounded_s = round(coord_s)

    q_diff = abs(rounded_q - coord_q)
    r_diff = abs(rounded_r - coord_r)
    s_diff = abs(rounded_s - coord_s)

    if q_diff > r_diff and q_diff > s_diff:
        rounded_q = -(rounded_r + rounded_s)
    elif r_diff > s_diff:
        rounded_r = -(rounded_q + rounded_s)
    else:
        rounded_s = -(rounded_q + rounded_r)

    return [rounded_q, rounded_r]


def get_hex_center(coordinates, hex_size):
    """
    convert hex coordinates to position (center of hex)
    """
    (coord_q, coord_r) = coordinates
    position_x = hex_size * 3. / 2 * coord_q
    position_y = hex_size * \
        (math.sqrt(3) / 2 * coord_q + math.sqrt(3) * coord_r)
    return [position_x + WIDTH / 2, position_y + HEIGHT / 2]


def axial_to_oddq(axial_coordinates):
    """
    convert axial coordinates to column row coordinates
    """
    cube_z = axial_coordinates[0] + axial_coordinates[1]
    col = axial_coordinates[0]
    row = int(cube_z + (axial_coordinates[0] - (axial_coordinates[0] & 1)) / 2)
    return [col, row]


def oddq_to_axial(oddq_coordinates):
    """
    convert column row coordinates to axial coordinates
    """
    x_coord = oddq_coordinates[1]
    z_coord = int(oddq_coordinates[0] - \
        (oddq_coordinates[1] - (oddq_coordinates[1] & 1)) / 2)
    y_coord = -x_coord - z_coord
    return [x_coord, y_coord]


def draw_planet_ellipse(svg, planet, center):
    """
    0. generate subgroup
    1. draw ellipse
    """
    (center_x, center_y) = center
    layer = svg.create_subgroup(planet.name, class_name='planet')
    layer.create_ellipse((planet.radius_x, planet.radius_y),
                         (center_x, center_y),
                         planet.colour,
                         planet.name + "_ellipse",
                         fill="none",
                         stroke_width="2")


def draw_hex_grid(parent, planets):
    """
    draw the hex grid
    """
    colored_hexes = []
    """
    for planet in planets:
        for index, coordinates in enumerate(planet.position_of_hexes):
            colored_hexes.append([coordinates, planet, index])
    """
    layer = parent.create_subgroup('hex_grid', class_name='hex_grid')
    for row in range(-5, 6):
        for column in range(-9, 10):
            coords = oddq_to_axial([row, column])
            """
            if abs(row + column) > max_distance_from_sun:
                continue
            """
            name_hex = "hex" + "_" + str(coords[0]) + "_" + str(coords[1])
            colour = "white"
            stroke_colour = "white"
            fill_opacity = "0"
            stroke_width = "0.5"
            stroke_opacity = "0.5"
            for hex_field in colored_hexes:
                if coords == hex_field[0]:
                    colour = hex_field[1].colour
                    stroke_colour = hex_field[1].colour
                    stroke_width = "1.5"
                    stroke_opacity = "1"
                    if hex_field[1].current_position == hex_field[2]:
                        fill_opacity = "1"
                    else:
                        fill_opacity = "0.25"
                    break

            hex_center = get_hex_center(coords, HEX_SIZE)
            layer.create_hex(
                name_hex,
                hex_center,
                coords,
                HEX_SIZE,
                colour,
                "hex",
                fill_opacity=fill_opacity,
                stroke_colour=stroke_colour,
                stroke_opacity=stroke_opacity,
                stroke_width=stroke_width
            )


def draw_sun(svg, size, radius):
    """
    draw the sun in the middle
    """
    (width, height) = size
    svg.create_circle((width / 2, height / 2), radius,
                      'sun', fill_colour='yellow')


def draw_gameboard(bg_image):
    """
    draw the main board
    """
    svg = Svg(width=str(WIDTH), height=str(HEIGHT), id_name="gameboard")
    svg.create_image(bg_image, width="1200", height="876", x_pos="0", y_pos="0")
    draw_hex_grid(svg, [])

    for planet in []:
        draw_planet_ellipse(svg, planet, (WIDTH / 2, HEIGHT / 2))

    draw_sun(svg, (WIDTH, HEIGHT), HEX_SIZE)
    svg_string = svg.get_string()
    return svg_string

def main():
    svg_string = draw_gameboard("static/auth/bg.jpeg")
    svg_filename = "printing_material/simon_gameboard.svg"
    with open(svg_filename, "w") as svg_file:
        svg_file.write(svg_string)
    subprocess.run(
        [
            "convert",
            "-density",
            "90",
            "printing_material/simon_gameboard.svg",
            "printing_material/simon_gameboard.pdf"
        ]
    )
    subprocess.run(
        [
            "pdfposter",
            "-m",
            "a4",
            "-p",
            "a1",
            "printing_material/simon_gameboard.pdf",
            "printing_material/simon_gameboard_split.pdf"
        ]
    )


if __name__ == '__main__':
    main()
