#!/usr/bin/env python
"""
generate the main gameboard
"""
import math
from .gamesettings import PLANETS
from .gamesettings import PLAYERS
from .svg_commands import Svg
from . import generate_svg_symbols

HEX_SIZE = 20
FONT_SIZE = 6

PADDING = 100
FONT_PADDING = 5

SHIP_WIDTH = 10
SHIP_HEIGHT = 15

SIZE_TIMEBOX = 30
NUMBER_TIMEBOXES_WIDTH = 31
NUMBER_TIMEBOXES_HEIGHT = 21
PADDING_TIMEBOXES = 20

WIDTH = NUMBER_TIMEBOXES_WIDTH * SIZE_TIMEBOX
HEIGHT = NUMBER_TIMEBOXES_HEIGHT * SIZE_TIMEBOX

assert 2 * (PLANETS[-1].radius_x + PADDING_TIMEBOXES +
            HEX_SIZE + SIZE_TIMEBOX) < WIDTH
assert 2 * (PLANETS[-1].radius_y + PADDING_TIMEBOXES +
            HEX_SIZE + SIZE_TIMEBOX) < HEIGHT


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


def print_hexes(positions, colour, parent, parentname):
    """
    print hexes of one planet
    """
    for index, position in enumerate(positions):
        hex_coordinates = get_hex_coordinates(position, HEX_SIZE)
        hex_center = get_hex_center(hex_coordinates, HEX_SIZE)
        parent.create_hex(parentname + "_" + str(index), hex_center,
                          hex_coordinates, HEX_SIZE, colour,
                          parentname + "_hex", fill_opacity="0.3")
        position_x = hex_center[0]
        position_y = hex_center[1] - HEX_SIZE / 2 - FONT_SIZE - FONT_PADDING
        content = str(int(hex_coordinates[0])) + "," + str(int(
            hex_coordinates[1])) + "," + str(int(- hex_coordinates[0] - hex_coordinates[1]))
        parent.create_text(
            parentname +
            "_coordinates_" +
            str(index),
            (position_x,
             position_y),
            content,
            font_size=FONT_SIZE,
            font_colour="#FFFFFF")


def draw_hex_grid(parent, center):
    """
    draw the hex grid
    """
    (center_x, center_y) = center
    colored_hexes = []
    for planet in PLANETS:
        degrees = list(range(0, planet.number_of_hexes))
        degrees[:] = [planet.offset + x * 2 * math.pi / planet.number_of_hexes for x in degrees]
        positions = [
            (planet.radius_x *
             math.cos(x) +
             center_x,
             planet.radius_y *
             math.sin(x) +
             center_y) for x in degrees]
        for index, position in enumerate(positions):
            hex_coordinates = get_hex_coordinates(position, HEX_SIZE)
            colored_hexes.append([hex_coordinates, planet, index])

    layer = parent.create_subgroup('hex_grid', class_name='hex_grid')
    for row in range(-7, 8):
        for column in range(-13, 14):
            coords = oddq_to_axial([row, column])
            if abs(coords[0]) < 2 and abs(coords[1]) < 2 and abs(coords[0] + coords[1]) < 2:
                continue
            name_hex = "hex" + "_" + str(coords[0]) + "_" + str(coords[1])
            colour = "{% get_colour planets " + str(coords[0]) + " " + str(coords[1]) + " %}"
            fill_opacity = "{% get_opacity planets " + str(coords[0]) + " " + str(coords[1]) + " %}"
            hex_center = get_hex_center(coords, HEX_SIZE)
            layer.create_hex(
                name_hex,
                hex_center,
                coords,
                HEX_SIZE,
                colour,
                "hex",
                fill_opacity=fill_opacity,
                stroke_colour="white",
                stroke_opacity="0.5",
                stroke_width="0.5"
            )
    
    coordinate_group = parent.create_subgroup('coordinates')
    coordinate_group.root.text = ("{% for planet in planets %} {% for coordinates in planet.position_of_hexes %}")
    content = "{{coordinates|at:0}},{{coordinates|at:1}},{% z_coord coordinates %}"
    text = coordinate_group.create_text(
        "coordinates_" + content,
        ["{% get_x_position_text coordinates " + "{} {} {}".format(HEX_SIZE, WIDTH, HEIGHT) +" %}",
        "{% get_y_position_text coordinates " + "{} {} {} {}".format(HEX_SIZE, WIDTH, HEIGHT, FONT_PADDING + FONT_SIZE) +" %}"],
        content,
        font_size = FONT_SIZE,
        font_colour="#FFFFFF"
    )
    text.root.tail = "{% endfor %}{% endfor %}"


def draw_timebox(position, size, name, time, parent):
    """
    draw one box of the timeline
    """
    (position_x, position_y) = position
    (width, height) = size
    fill_colour = "#FFFFFF"
    if time % 10 == 0:
        fill_colour = "#AAAAAA"

    additional_arguments = {
        'time': str(time),
        'class': 'timebox'
    }

    parent.create_rectangle((position_x, position_y), (width, height),
                            name, fill_colour=fill_colour,
                            stroke_colour="#000000",
                            stroke_width=1,
                            fill_opacity=1,
                            additional_arguments=additional_arguments)
    parent.create_text(
        "timebox_text_" + str(time),
        (position_x + width / 2, position_y + height / 2 + 4),
        str(time), font_size=8
    )

    #events = []
    #if time % 20 == 0:
    #    events.append("planet_rotation")

    #draw_events_for_one_timestep(
    #    (position_x, position_y), (width, height), events, time, parent)


def draw_event(center, radius, event, time, parent):
    """
    draw an event marker on the timeline
    """
    (center_x, center_y) = center
    additional_arguments = {
        'time': str(time),
        'event': event,
        'class': 'event'
    }
    parent.create_circle((center_x, center_y), radius, str(time) + "_" + event,
                         fill_colour='#00FFFF',
                         additional_arguments=additional_arguments)


def draw_events_for_one_timestep(
        position,
        size,
        events,
        time,
        parent):
    """
    draw all events for one timestep
    """
    (position_x, position_y) = position
    (width, height) = size
    radius = min(width, height) / 4

    for index, event in enumerate(events):
        center_x = 0
        center_y = 0
        if index == 0:
            center_x = position_x + width / 4
            center_y = position_y + height / 4
        elif index == 1:
            center_x = position_x + 3 * width / 4
            center_y = position_y + height / 4
        elif index == 2:
            center_x = position_x + width / 4
            center_y = position_y + 3 * height / 4
        elif index == 3:
            center_x = position_x + 3 * width / 4
            center_y = position_y + 3 * height / 4
        else:
            print("error: too many events")

        draw_event((center_x, center_y), radius, event, str(time), parent)


def draw_timeline(svg):
    """
    create the whole timeline
    """
    layer = svg.create_subgroup("timeline")
    for i in range(0, 31):
        draw_timebox((i * SIZE_TIMEBOX, 0),
                     (SIZE_TIMEBOX, SIZE_TIMEBOX),
                     "timebox_" + str(i), i, layer)
    for i in range(31, 51):
        draw_timebox((30 * SIZE_TIMEBOX, (i - 30) * SIZE_TIMEBOX),
                     (SIZE_TIMEBOX, SIZE_TIMEBOX),
                     "timebox_" + str(i), i, layer)
    for i in range(51, 81):
        draw_timebox(((80 - i) * SIZE_TIMEBOX, 20 * SIZE_TIMEBOX),
                     (SIZE_TIMEBOX, SIZE_TIMEBOX),
                     "timebox_" + str(i), i, layer)
    for i in range(81, 100):
        draw_timebox((0, (100 - i) * SIZE_TIMEBOX),
                     (SIZE_TIMEBOX, SIZE_TIMEBOX),
                     "timebox_" + str(i), i, layer)


def draw_sun(svg, size, radius):
    """
    draw the sun in the middle
    """
    (width, height) = size
    svg.create_circle((width / 2, height / 2), radius,
                      'sun', fill_colour='yellow')


def draw_player_ships(svg):
    """
    draw ships of all players
    """
    players_group = svg.create_subgroup('player_ships')
    players_group.root.text = "{% for player in players %}"
    rect = players_group.create_rectangle(("{% get_x_position_ship player " + "{} {} {}".format(HEX_SIZE, WIDTH, HEIGHT) + " %}",
                                           "{% get_y_position_ship player " + "{} {} {}".format(HEX_SIZE, WIDTH, HEIGHT) + " %}"),
                                           (SHIP_WIDTH, SHIP_HEIGHT),
                                           "ship_{{ player.user.get_username }}",
                                           fill_colour="{{ player.colour }}",
                                           stroke_colour="black",
                                           additional_arguments={'class': 'ship'})
    rect.root.tail = "{% endfor %}"


def main():
    """
    draw the main board
    """
    svg = Svg(width=str(WIDTH), height=str(HEIGHT), id_name="gameboard")
    generate_svg_symbols.add_posibility_for_disc_3d(svg)
    svg.create_image("/static/auth/bg.jpeg", width="1200", height="876", x_pos="0", y_pos="0")
    draw_timeline(svg)
    draw_hex_grid(svg, (WIDTH / 2, HEIGHT / 2))
    for planet in PLANETS:
        draw_planet_ellipse(svg, planet, (WIDTH / 2, HEIGHT / 2))

    draw_sun(svg, (WIDTH, HEIGHT), HEX_SIZE)
    draw_player_ships(svg)
    svg_string = svg.get_string()
    #print("gameboard")
    with open("gameboard.svg", "w") as out_file:
        out_file.write(svg_string)


if __name__ == '__main__':
    main()
