#!/usr/bin/env python
"""
generate the planet market
"""

from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg import generate_svg_symbols

def get_symbol_name(resource):
    if resource is '0':
        return 'resource_placeholder'
    elif resource is '1':
        return 'red_cross'
    elif resource is '2':
        return 'radioactive'
    elif resource is '3':
        return 'food'
    elif resource is '4':
        return 'water'
    elif resource is '5':
        return 'building_resource'


def create_playerboard(svg, player, position):
    """
    create a playerboard in the svg at position
    Arguments:
        svg {Svg} -- root svg element
        player {Player} -- for which player
        position {[x, y]} -- position where the playerboard will be drawn
    """
    playername = player.user.get_username()
    subgroup = svg.create_subgroup("playerboard_" + playername)
    subgroup.create_rectangle(
        [position[0], position[1]],
        [140, 70],
        "background_hangar_" + str(playername),
        stroke_colour="black", fill_opacity="1",
        fill_colour=player.colour,
        additional_arguments={
            "rx" : "10",
            "ry" : "10"
        }
    )
    font_size = 8
    subgroup.create_text(
        "playerboard_name_" + playername,
        [position[0] + 10, position[1] + 10 + font_size],
        playername,
        text_anchor="left",
        font_size=font_size,
    )
    subgroup.create_rectangle(
        [position[0] + 10, position[1] + 30],
        [50, 30],
        "coin_background_" + playername,
        stroke_colour="black",
        fill_colour="white",
        additional_arguments={
            "rx": "10",
            "ry": "10"
        }
    )
    subgroup.use_symbol(
        "coin",
        "coin_" + playername,
        [position[0] + 15, position[1] + 35]
    )
    subgroup.create_text(
        "coins_" + playername,
        [position[0] + 55, position[1] + 40 + font_size],
        str(player.money),
        text_anchor="end",
        font_size=font_size
    )

    for index, resource in enumerate(player.resources):
        row = index % 3
        column = (index - row)/3
        subgroup.use_symbol(
            get_symbol_name(resource),
            "resource_{}_{}".format(playername, row + column*2),
            [
                position[0] + 70 + column*20,
                position[1] + 5 + row*20
            ]
        )

def add_symbols(svg):
    """add symbols to the svg

    Arguments:
        svg {Svg} -- root svg
    """
    generate_svg_symbols.add_posibility_for_empty_res(svg)
    generate_svg_symbols.add_posibility_for_red_cross(svg)
    generate_svg_symbols.add_posibility_for_radioactive(svg)
    generate_svg_symbols.add_posibility_for_food(svg)
    generate_svg_symbols.add_posibility_for_water(svg)
    generate_svg_symbols.add_posibility_for_building_res(svg)
    generate_svg_symbols.add_posibility_for_coin(svg)


def draw_player_boards(players):
    """
    draw the player board
    """

    svg = Svg(width=640, height=80, id_name="playerboards")
    add_symbols(svg)
    for index, player in enumerate(players):
        create_playerboard(svg, player, [10 + 160*index, 5])

    svg_string = svg.get_string()

    return svg_string

if __name__ == '__main__':
    pass
