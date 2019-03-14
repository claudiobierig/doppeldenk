#!/usr/bin/env python
"""
generate the planet market
"""

from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg import generate_svg_symbols
from spacetrading.logic import move

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


def create_playerboard(svg, player, game, position, active):
    """
    create a playerboard in the svg at position
    Arguments:
        svg {Svg} -- root svg element
        player {Player} -- for which player
        game {Game} -- game instance to compute the number of points
        position {[x, y]} -- position where the playerboard will be drawn
        active {bool} -- is the player the active player
    """
    playername = player.user.get_username()
    points = move.compute_points(game, player.player_number)
    subgroup = svg.create_subgroup("playerboard_" + playername)
    font_colour = "black"
    if active:
        font_colour = "red"
    
    subgroup.create_rectangle(
        [position[0], position[1]],
        [220, 110],
        "background_hangar_" + str(playername),
        stroke_colour="black", fill_opacity="1",
        fill_colour=player.colour,
        additional_arguments={
            "rx" : "10",
            "ry" : "10"
        }
    )
    font_size = 12
    
    subgroup.create_rectangle(
        [position[0] + 10, position[1] + 10],
        [100, 95],
        "text_background_" + playername,
        stroke_colour="black",
        fill_colour="white",
        additional_arguments={
            "rx": "10",
            "ry": "10"
        }
    )
    
    subgroup.create_text(
        "playerboard_name_" + playername,
        [position[0] + 20, position[1] + 20 + font_size],
        playername,
        text_anchor="start",
        font_size=font_size,
        font_colour=font_colour
    )
    subgroup.create_text(
        "points_" + playername,
        [position[0] + 20, position[1] + 50 + font_size],
        "{} points".format(points),
        text_anchor="start",
        font_size=font_size
    )

    
    subgroup.use_symbol(
        "coin",
        "coin_" + playername,
        [(position[0] + 15)*2/3, (position[1] + 72.5)*2/3],
        additional_arguments={"transform": "scale(1.5 1.5)"}
    )
    subgroup.create_text(
        "coins_" + playername,
        [position[0] + 50, position[1] + 70 + (35+font_size)/2],
        str(player.money),
        text_anchor="start",
        font_size=font_size
    )

    for index, resource in enumerate(player.resources):
        row = index % 3
        column = (index - row)/3
        subgroup.use_symbol(
            get_symbol_name(resource),
            "resource_{}_{}".format(playername, row + column*2),
            [
                (position[0] + 120 + column*30)*2/3,
                (position[1] + 10 + row*30)*2/3
            ],
            additional_arguments={"transform": "scale(1.5 1.5)"}
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


def draw_player_boards(players, game):
    """
    draw the player board
    """

    svg = Svg(width=960, height=120, id_name="playerboards")
    add_symbols(svg)
    active_player = move.get_active_player(players)
    for index, player in enumerate(players):
        active = False
        if active_player.player_number == player.player_number:
            active = True
        create_playerboard(svg, player, game, [10 + 240*index, 5], active)

    svg_string = svg.get_string()

    return svg_string

if __name__ == '__main__':
    pass
