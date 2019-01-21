#!/usr/bin/env python
"""
generate a player board
"""
from .gamesettings import PLAYERS
from .svg_commands import Svg
from . import generate_svg_symbols

WIDTH = 160
HEIGHT = 320

def create_playerboard(svg, player, position):
    """
    create a playerboard in the svg at position
    Arguments:
        svg {Svg} -- root svg element
        player {Player} -- for which player
        position {[x, y]} -- position where the playerboard will be drawn
    """
    subgroup = svg.create_subgroup("playerboard_" + player.name)
    subgroup.create_rectangle(
        [position[0], position[1]],
        [WIDTH - 2*position[0], 70],
        "background_hangar_" + str(player.name),
        stroke_colour="black", fill_opacity="0.4",
        fill_colour=player.colour,
        additional_arguments={
            "rx" : "10",
            "ry" : "10"
        }
    )
    font_size = 8
    subgroup.create_text(
        "playerboard_name_" + player.name,
        [position[0] + 10, position[1] + 10 + font_size],
        player.name,
        text_anchor="left",
        font_size=font_size,
    )
    subgroup.create_rectangle(
        [position[0] + 10, position[1] + 30],
        [50, 30],
        "coin_background_" + player.name,
        stroke_colour="black",
        fill_colour="white",
        additional_arguments={
            "rx": "10",
            "ry": "10"
        }
    )
    subgroup.use_symbol(
        "coin",
        "coin_" + player.name,
        [position[0] + 15, position[1] + 35]
    )
    subgroup.create_text(
        "coins_" + player.name,
        [position[0] + 55, position[1] + 40 + font_size],
        "0",
        text_anchor="end",
        font_size=font_size
    )
    for row in range(3):
        for column in range(3):
            subgroup.use_symbol(
                "resource_placeholder",
                "resource_{}_{}".format(player.name, row + column*2),
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


def main():
    """
    draw the player board
    """
    svg = Svg(width=str(WIDTH), height=str(HEIGHT), id_name="playerboard")
    add_symbols(svg)
    for index, player in enumerate(PLAYERS):
        create_playerboard(svg, player, [10, 5 + 80*index])

    svg_string = svg.get_string()

    #print(svg_string)
    with open("playerboard.svg", "w") as out_file:
        out_file.write(svg_string)

    return svg_string


if __name__ == '__main__':
    main()
