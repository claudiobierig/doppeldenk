#!/usr/bin/env python
"""
generate the planet market
"""

from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg import generate_svg_symbols


def create_playerboard(svg, colour, playername, position):
    """
    create a playerboard in the svg with fill_colour colour at position
    """
    subgroup = svg.create_subgroup(
        "playerboard_{}".format(playername)
    )
    subgroup.create_rectangle(
        [position[0], position[1]],
        [340, 230],
        "background_hangar_{}".format(playername),
        stroke_colour="black", fill_opacity="1",
        fill_colour=colour,
        additional_arguments={
            "rx": "20",
            "ry": "20"
        }
    )

    for index, resource in enumerate(['1', '2', '3', '4', '5', 'coin']):
        column = index % 3
        row = (index - column)/3
        subgroup.create_rectangle(
            [position[0] + 10 + 110*column, position[1] + 10 + 110*row],
            [100, 100],
            "background_resource_{}".format(resource),
            stroke_colour="black", fill_opacity="1",
            fill_colour="#DDD",
            stroke_width=3,
            additional_arguments={
                "rx": "10",
                "ry": "10"
            }
        )
        subgroup.use_symbol(
            generate_svg_symbols.get_symbol_name(resource),
            "resource_{}_{}".format(resource, playername),
            [
                (position[0] + 45 + 110*column)*2/3,
                (position[1] + 15 + 110*row)*2/3
            ],
            additional_arguments={"transform": "scale(1.5 1.5)"}
        )
        subgroup.create_rectangle(
            [position[0] + 10 + 110*column, position[1] + 49 + 110*row],
            [100, 2],
            "separator_resource_{}".format(resource),
            stroke_colour="black", fill_opacity="1",
            fill_colour="black"
        )


def add_symbols(svg):
    """add symbols to the svg

    Arguments:
        svg {Svg} -- root svg
    """
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
    svg = Svg(width=680, height=460, id_name="playerboards")
    add_symbols(svg)
    for index, player in enumerate(players):
        create_playerboard(svg, player.colour, str(index), [
                           340*(index % 2), 230*int(index/2)])

    svg_string = svg.get_string()

    return svg_string


if __name__ == '__main__':
    pass
