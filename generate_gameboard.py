#!/usr/bin/env python
"""
generate the main gameboard
"""
import math
from gamesettings import PLANETS
from gamesettings import PLAYERS
from svg_commands import Svg
import generate_svg_symbols

HEX_SIZE = 20
FONT_SIZE = 6

PADDING = 100
FONT_PADDING = 5

SHIP_WIDTH = 10
SHIP_HEIGHT = 20

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
    (position_x, position_y) = position
    coord_q = (2. / 3 * position_x) / hex_size
    coord_r = (-1. / 3 * position_x + math.sqrt(3) / 3 * position_y) / hex_size
    return [round(coord_q), round(coord_r)]


def get_hex_center(coordinates, hex_size):
    """
    convert hex coordinates to position (center of hex)
    """
    (coord_q, coord_r) = coordinates
    position_x = hex_size * 3. / 2 * coord_q
    position_y = hex_size * (math.sqrt(3) / 2 * coord_q + math.sqrt(3) * coord_r)
    return [position_x, position_y]


def draw_planet(svg, planet, center):
    """
    0. generate subgroup
    1. draw ellipse
    2. compute length of elipse
    3. compute where hexes should be
    4. draw hexes and coordinates
    """
    (center_x, center_y) = center
    layer = svg.create_subgroup(planet.name, class_name='planet')
    layer.create_ellipse((planet.radius_x, planet.radius_y),
                         (center_x, center_y),
                         planet.colour,
                         planet.name + "_ellipse",
                         fill="none")

    # compute degree where the hexes should be
    degrees = range(0, planet.number_of_hexes)
    degrees[:] = [x * 2 * math.pi / planet.number_of_hexes for x in degrees]
    positions = [
        (planet.radius_x *
         math.cos(x) +
         center_x,
         planet.radius_y *
         math.sin(x) +
         center_y) for x in degrees]
    print_hexes(positions, planet.colour, layer, planet.name)


def print_hexes(positions, colour, parent, parentname):
    """
    print hexes of one planet
    """
    for index, position in enumerate(positions):
        hex_coordinates = get_hex_coordinates(position, HEX_SIZE)
        hex_center = get_hex_center(hex_coordinates, HEX_SIZE)
        parent.create_hex(parentname + "_" + str(index), hex_center,
                          hex_coordinates, HEX_SIZE, colour,
                          parentname + "_hex")
        position_x = hex_center[0]
        position_y = hex_center[1] - HEX_SIZE / 2 - FONT_SIZE - FONT_PADDING
        content = str(int(hex_coordinates[0])) + "," + str(int(
            hex_coordinates[1])) + "," + str(int(- hex_coordinates[0] - hex_coordinates[1]))
        parent.create_text((position_x, position_y), content, font_size=FONT_SIZE,
                           font_colour="#FFFFFF")


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
    parent.create_text((position_x + width / 2, position_y + height / 2 + 4), str(time),
                       font_size=8)

    events = []
    if time % 20 == 0:
        events.append("planet_rotation")

    draw_events_for_one_timestep((position_x, position_y), (width, height), events, time, parent)


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
            print "error: too many events"

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
    svg.create_circle((width / 2, height / 2), radius, 'sun', fill_colour='yellow')


def draw_players(svg):
    """
    draw ships and timemarkers of all players
    """
    players_group = svg.create_subgroup('players')
    for index, player in enumerate(PLAYERS):
        player_group = players_group.create_subgroup(player.name)
        additional_arguments_disc = {
            'time': '0',
            'class': 'timemarker'
        }
        player_group.use_symbol("disc_3d", "timemarker_" + player.name,
                                (0, 15 - index*4), fill_colour=player.colour,
                                additional_arguments=additional_arguments_disc)
        player_group.create_rectangle((index * (SHIP_WIDTH + 10) + 50, 50),
                                      (SHIP_WIDTH, SHIP_HEIGHT),
                                      "ship_" + player.name,
                                      fill_colour=player.colour,
                                      additional_arguments={'class': 'ship'})


def main():
    """
    draw the main board
    """
    svg = Svg(width=str(WIDTH), height=str(HEIGHT), id_name="gameboard")
    generate_svg_symbols.add_posibility_for_disc_3d(svg)
    svg.create_image("bg.jpeg")
    draw_timeline(svg)
    for planet in PLANETS:
        draw_planet(svg, planet, (WIDTH / 2, HEIGHT / 2))

    draw_sun(svg, (WIDTH, HEIGHT), HEX_SIZE)
    draw_players(svg)
    svg_string = svg.get_string()
    print svg_string
    with open("gameboard.svg", "w") as out_file:
        out_file.write(svg_string)


if __name__ == '__main__':
    main()