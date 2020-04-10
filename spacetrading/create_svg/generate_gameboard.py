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
    z_coord = int(oddq_coordinates[0] -
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


def draw_hex_grid(parent, planets, user_active):
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
            stroke_colour = "white"
            fill_opacity = "0"
            stroke_width = "0.5"
            stroke_opacity = "0.5"
            hex_center = get_hex_center(coords, HEX_SIZE)
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
                stroke_width=stroke_width,
                enableOnClick=user_active
            )


def draw_timebox(position, size, name, time, parent, user_active):
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
    if user_active:
        additional_arguments["onClick"] = "clickTimebox(this)"

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


def draw_timeline(svg, user_active):
    """
    create the whole timeline
    """
    layer = svg.create_subgroup("timeline")
    for i in range(0, 31):
        draw_timebox((i * SIZE_TIMEBOX, 0),
                     (SIZE_TIMEBOX, SIZE_TIMEBOX),
                     "timebox_" + str(i), i, layer, user_active)
    for i in range(31, 51):
        draw_timebox((30 * SIZE_TIMEBOX, (i - 30) * SIZE_TIMEBOX),
                     (SIZE_TIMEBOX, SIZE_TIMEBOX),
                     "timebox_" + str(i), i, layer, user_active)
    for i in range(51, 81):
        draw_timebox(((80 - i) * SIZE_TIMEBOX, 20 * SIZE_TIMEBOX),
                     (SIZE_TIMEBOX, SIZE_TIMEBOX),
                     "timebox_" + str(i), i, layer, user_active)
    for i in range(81, 100):
        draw_timebox((0, (100 - i) * SIZE_TIMEBOX),
                     (SIZE_TIMEBOX, SIZE_TIMEBOX),
                     "timebox_" + str(i), i, layer, user_active)


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
                [hex_center[0]+player.ship_offset[0],
                    hex_center[1]+player.ship_offset[1]],
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
    elif 80 < time_space < 100:
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
        if player.last_move >= 0 and not player.has_passed:
            timemarkers.append(
                [
                    player.time_spent,
                    player.last_move,
                    player.colour,
                    "player_{}".format(player.player_number),
                    'disc_3d'
                ]
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
    if game.midgame_scoring:
        timemarkers.append(
            [
                game.midgame_scoring_event_time,
                game.midgame_scoring_event_move,
                "blue",
                "scoring",
                "square_3d"
            ]
        )
    if game.add_demand:
        timemarkers.append(
            [
                game.add_demand_event_time,
                game.add_demand_event_move,
                "green",
                "add_demand",
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


def draw_playerhelp(svg, position, midgame_scoring=True, add_demand=True):
    """
    draw playerhelp
    """
    font_size = 8
    playerhelps = [
        ("planet_rotation", "Planet rotation", "yellow"),
        ("offer_demand", "Offer Demand", "orange")
    ]
    if midgame_scoring:
        playerhelps.append(("midgame_scoring", "Midgame scoring", "blue"))
    if add_demand:
        playerhelps.append(("add_demand", "Add Demand", "green"))

    for index, (id_help, text, colour) in enumerate(playerhelps):
        svg.create_rectangle(
            [position[0], position[1] + 25*index],
            [90, 20],
            f"playerhelp_{id_help}_rectangle",
            fill_colour=colour,
            stroke_colour="black",
            additional_arguments={
                "rx": "10",
                "ry": "10"
            }
        )
        svg.create_text(
            f"playerhelp_{id_help}_text",
            [position[0] + 45, position[1] + 25*index + 10 + font_size/2],
            text,
            font_size=8,
            font_colour="#000000",
            text_align="center",
            text_anchor="middle"
        )


def draw_gameboard(game, planets, players, user_active, bg_image="/static/auth/bg.jpeg", printing_material=False):
    """
    draw the main board
    """
    svg = Svg(width=str(WIDTH), height=str(HEIGHT), id_name="gameboard")
    generate_svg_symbols.add_posibility_for_disc_3d(svg)
    generate_svg_symbols.add_posibility_for_square_3d(svg)
    svg.create_image(bg_image, width="1200",
                     height="876", x_pos="0", y_pos="0")
    draw_timeline(svg, user_active)
    draw_hex_grid(svg, planets, user_active)

    for planet in planets:
        draw_planet_ellipse(svg, planet, (WIDTH / 2, HEIGHT / 2))

    draw_sun(svg, (WIDTH, HEIGHT), HEX_SIZE)
    if not printing_material:
        draw_player_ships(svg, players)
        draw_timemarkers(svg, game, players)
    draw_playerhelp(svg, [WIDTH - 130, 40], game.midgame_scoring, game.add_demand)
    svg_string = svg.get_string()

    return svg_string


if __name__ == '__main__':
    pass
