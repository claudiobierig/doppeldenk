#!/usr/bin/env python
"""
generate the main gameboard
"""
import math
import operator
from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg import generate_svg_symbols

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


def draw_hex_grid(parent, planets):
    """
    draw the hex grid
    """
    colored_hexes = []
    for planet in planets:
        for index, coordinates in enumerate(planet.position_of_hexes):
            colored_hexes.append([coordinates, planet, index])

    layer = parent.create_subgroup('hex_grid', class_name='hex_grid')
    for row in range(-7, 8):
        for column in range(-13, 14):
            coords = oddq_to_axial([row, column])
            if abs(coords[0]) < 2 and abs(coords[1]) < 2 and abs(coords[0] + coords[1]) < 2:
                continue
            name_hex = "hex" + "_" + str(coords[0]) + "_" + str(coords[1])
            colour = "white"
            fill_opacity = "0"
            for hex_field in colored_hexes:
                if coords == hex_field[0]:
                    colour = hex_field[1].colour
                    if hex_field[1].current_position == hex_field[2]:
                        fill_opacity = "1"
                    else:
                        fill_opacity = "0.2"
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
                stroke_colour="white",
                stroke_opacity="0.5",
                stroke_width="0.5"
            )
    
    coordinate_group = parent.create_subgroup('coordinates')
    
    for hex_field in colored_hexes:
        content = "{},{},{}".format(hex_field[0][0], hex_field[0][1], -hex_field[0][0] - hex_field[0][1])
        hex_center = get_hex_center(hex_field[0], HEX_SIZE)
        coordinate_group.create_text(
            "coordinates_{}".format(content),
            [hex_center[0], hex_center[1] - HEX_SIZE/2 - FONT_PADDING - FONT_SIZE],
            content,
            font_size=FONT_SIZE,
            font_colour="#FFFFFF"
        )

    return

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


def draw_player_ships(svg, players):
    """
    draw ships of all players
    """
    players_group = svg.create_subgroup('player_ships')
    for player in players:
        if player.last_move >= 0:
            hex_center = get_hex_center(player.ship_position, HEX_SIZE)
            players_group.create_rectangle(
                [hex_center[0]+player.ship_offset[0], hex_center[1]+player.ship_offset[1]],
                (SHIP_WIDTH, SHIP_HEIGHT),
                "ship_{}".format(player.user.get_username()),
                fill_colour=player.colour,
                stroke_colour="black"
            )

def get_timemarker_position(time_spent, stack_position):
    """
    given the time_spent and the number of timemarkers below in the stack
    return the position where to print the timemarker
    """
    time_space = time_spent % 100
    if 0 <= time_space <= 30:
        x_pos = time_space * SIZE_TIMEBOX
        y_pos = 15
    elif 30 < time_space <= 50:
        x_pos = 30 * SIZE_TIMEBOX
        y_pos = 15 + (time_space - 30) * SIZE_TIMEBOX
    elif 50 < time_space <= 80:
        x_pos = (80 - time_space) * SIZE_TIMEBOX
        y_pos = 15 + 20*SIZE_TIMEBOX
    elif 81 < time_space < 100:
        x_pos = 0
        y_pos = 15 + (100 - time_space) * SIZE_TIMEBOX
    y_pos = y_pos - stack_position*4
    return [x_pos, y_pos]

def draw_timemarkers(svg, game, players):
    """
    draw timemarkers of all players
    """
    timemarkers = []
    for player in players:
        if player.last_move >= 0:
            timemarkers.append(
                [player.time_spent, player.last_move, player.colour, player.user.get_username(), 'disc_3d']
            )
    timemarkers.append(
        [
            game.planet_rotation_event_time,
            game.planet_rotation_event_move,
            "yellow",
            "planet_rotation",
            "square_3d"
        ]
    )
    timemarkers.append(
        [
            game.offer_demand_event_time,
            game.offer_demand_event_move,
            "orange",
            "offer_demand",
            "square_3d"
        ]
    )
    
    timemarkers.sort(key=operator.itemgetter(0, 1))
    timemarkers_svg = svg.create_subgroup('timemarkers')
    stack_position = 0
    last_timemarker = None
    for timemarker in timemarkers:
        if last_timemarker is timemarker[0]:
            stack_position = stack_position + 1
        else:
            stack_position = 0
        last_timemarker = timemarker[0]
        timemarkers_svg.use_symbol(
            timemarker[4],
            'timemarker_{}'.format(timemarker[3]),
            position=get_timemarker_position(timemarker[0], stack_position),
            fill_colour=timemarker[2]
        )

def draw_playerhelp(svg, position):
    """
    draw playerhelp
    """
    svg.create_rectangle(
        position,
        [90, 20],
        "playerhelp",
        fill_colour="yellow",
        stroke_colour="black",
        additional_arguments={
            "rx": "10",
            "ry": "10"
        }
    )
    svg.create_text(
        "player_help_planet_rotation",
        [position[0] + 45, position[1] + 10 + 4],
        "Planet rotation",
        font_size=8,
        font_colour="#000000",
        text_align="center",
        text_anchor="middle"
    )
    svg.create_rectangle(
        [position[0], position[1] + 25],
        [90, 20],
        "playerhelp",
        fill_colour="orange",
        stroke_colour="black",
        additional_arguments={
            "rx": "10",
            "ry": "10"
        }
    )
    svg.create_text(
        "player_help_offer_demand",
        [position[0] + 45, position[1] + 35 + 4],
        "Offer Demand",
        font_size=8,
        font_colour="#000000",
        text_align="center",
        text_anchor="middle"
    )

def draw_influence_tracks(svg, game, planets, players):
    """
    draw the influence tracks including the markers of the players
    """
    planet_tracks_svg = svg.create_subgroup('planet_influence_tracks')
    for planet_number, planet in enumerate(planets):
        for field in range(0, 21):
            x_pos = WIDTH + planet_number*SIZE_TIMEBOX
            y_pos = HEIGHT - (field + 1)*SIZE_TIMEBOX
            planet_tracks_svg.create_rectangle(
                [x_pos, y_pos],
                [SIZE_TIMEBOX, SIZE_TIMEBOX],
                "{}_influence_{}".format(planet.name, field),
                fill_colour=planet.colour,
                stroke_colour="black"
            )
            if field % 10 == 0:
                planet_tracks_svg.create_rectangle(
                    [x_pos, y_pos],
                    [SIZE_TIMEBOX, SIZE_TIMEBOX],
                    "{}_influence_{}_transperent".format(planet.name, field),
                    fill_colour="black",
                    fill_opacity="0.4"
                )
            planet_tracks_svg.create_text(
                "{}_influence_{}_text".format(planet.name, field),
                (x_pos + SIZE_TIMEBOX / 2, y_pos + SIZE_TIMEBOX / 2 + 4),
                str(field),
                font_size=8
            )
        planet_points = []
        for player_number, player in enumerate(players):
            points = game.planet_influence_track[planet_number][player_number]
            #TODO: points larger than 20
            stack_position = planet_points.count(points)
            planet_points.append(points)
            x_pos = WIDTH + planet_number*SIZE_TIMEBOX
            y_pos = (20 - points)*SIZE_TIMEBOX + 15 - 4*stack_position
            planet_tracks_svg.use_symbol(
                'disc_3d',
                'influence_marker_{}_{}'.format(player.user.get_username(), planet.name),
                position=[x_pos, y_pos],
                fill_colour=player.colour
            )


def draw_gameboard(game, planets, players):
    """
    draw the main board
    """
    svg = Svg(width=str(WIDTH + len(planets)*SIZE_TIMEBOX), height=str(HEIGHT), id_name="gameboard")
    generate_svg_symbols.add_posibility_for_disc_3d(svg)
    generate_svg_symbols.add_posibility_for_square_3d(svg)
    svg.create_image("/static/auth/bg.jpeg", width="1200", height="876", x_pos="0", y_pos="0")
    draw_timeline(svg)
    draw_hex_grid(svg, planets)

    for planet in planets:
        draw_planet_ellipse(svg, planet, (WIDTH / 2, HEIGHT / 2))

    draw_sun(svg, (WIDTH, HEIGHT), HEX_SIZE)
    draw_player_ships(svg, players)
    draw_timemarkers(svg, game, players)
    draw_playerhelp(svg, [WIDTH - 130, 40])
    draw_influence_tracks(svg, game, planets, players)
    svg_string = svg.get_string()

    return svg_string


if __name__ == '__main__':
    pass
