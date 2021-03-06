#!/usr/bin/env python
"""
generate the planet market
"""

from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg import generate_svg_symbols
from spacetrading.logic import move


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
    playernumber = str(player.player_number)
    points = move.compute_points(game, player)
    if game.midgame_scoring:
        if game.midgame_scoring_event_time == 50:
            points = points + move.compute_points(game, player, [2, 1])
        else:
            points = "{} ({})".format(points, player.points)

    additional_arguments = {
        "active": str(active),
        "money": str(player.money),
        "resource_1": str(player.resources[0]),
        "resource_2": str(player.resources[1]),
        "resource_3": str(player.resources[2]),
        "resource_4": str(player.resources[3]),
        "resource_5": str(player.resources[4])
    }
    subgroup = svg.create_subgroup(
        "playerboard_" + playernumber,
        additional_arguments=additional_arguments
    )
    font_colour = "black"
    if active:
        font_colour = "red"

    subgroup.create_rectangle(
        [position[0], position[1]],
        [220, 110],
        "background_hangar_" + str(playernumber),
        stroke_colour="black", fill_opacity="1",
        fill_colour=player.colour,
        additional_arguments={
            "rx": "10",
            "ry": "10"
        }
    )
    font_size = 12

    subgroup.create_rectangle(
        [position[0] + 10, position[1] + 10],
        [100, 95],
        "playerboard_text_background_" + playernumber,
        stroke_colour="black",
        fill_colour="white",
        additional_arguments={
            "rx": "10",
            "ry": "10"
        }
    )

    subgroup.create_text(
        "playerboard_name_" + playernumber,
        [position[0] + 20, position[1] + 20 + font_size],
        playername,
        text_anchor="start",
        font_size=font_size,
        font_colour=font_colour
    )
    subgroup.create_text(
        "points_" + playernumber,
        [position[0] + 20, position[1] + 50 + font_size],
        "{} points".format(points),
        text_anchor="start",
        font_size=font_size
    )

    subgroup.use_symbol(
        "coin",
        "coin_" + playernumber,
        [(position[0] + 15)*2/3, (position[1] + 72.5)*2/3],
        additional_arguments={"transform": "scale(1.5 1.5)"}
    )
    subgroup.create_text(
        "coins_" + playernumber,
        [position[0] + 50, position[1] + 70 + (35+font_size)/2],
        str(player.money),
        text_anchor="start",
        font_size=font_size
    )

    for index, resource in enumerate(['1', '2', '3', '4', '5']):
        column = index % 3
        row = (index - column)/3
        subgroup.use_symbol(
            generate_svg_symbols.get_symbol_name(resource),
            "resource_{}_{}".format(resource, playernumber),
            [
                (position[0] + 120 + column*30)*2/3,
                (position[1] + 10 + row*50)*2/3
            ],
            additional_arguments={"transform": "scale(1.5 1.5)"}
        )
        subgroup.create_text(
            "resource_amount_{}_{}".format(resource, playernumber),
            [
                (position[0] + 135 + column*30),
                (position[1] + 42 + row*50 + font_size)
            ],
            str(player.resources[index]),
            font_size=font_size
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

    svg = Svg(width=480, height=240, id_name="playerboards")
    add_symbols(svg)
    active_player = move.get_active_player(players, game.finish_time)
    for index, player in enumerate(players):
        active = False
        if active_player is not None and active_player.player_number == player.player_number:
            active = True
        create_playerboard(svg, player, game, [
                           10 + 240*(index % 2), 5 + 120*int(index/2)], active)

    svg_string = svg.get_string()

    return svg_string


if __name__ == '__main__':
    pass
