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


def draw_resource(svg, resource, index, planet, player):
    x_pos = 10 + index*40
    y_pos = 10
    svg.use_symbol(
        get_symbol_name(resource),
        'trade_modal_{}'.format(get_symbol_name(resource)),
        position=[x_pos, y_pos]
    )

def draw_trade_modal(players, planets):
    """
    draw the trading board
    """

    svg = Svg(width=400, height=400, id_name="trade_svg")
    add_symbols(svg)
    active_player = move.get_active_player(players)
    current_planet = None
    for planet in planets:
        if active_player.ship_position == planet.position_of_hexes[planet.current_position]:
            current_planet = planet
            break
    
    if current_planet is None:
        return "Can't trade in middle of space."
    
    for index, resource in enumerate(['1', '2', '3', '4', '5']):
        draw_resource(svg, resource, index, current_planet, active_player)

    svg.create_rectangle(
        [10, 60],
        [380, 380],
        "test",
        fill_colour=current_planet.colour
    )

    svg_string = svg.get_string()

    return svg_string

if __name__ == '__main__':
    pass
