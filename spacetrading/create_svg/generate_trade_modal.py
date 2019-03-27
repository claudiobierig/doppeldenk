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


def draw_resource(svg, position, resource, direction):
    x_pos = position[0]
    y_pos = position[1]
    svg.use_symbol(
        get_symbol_name(resource),
        'trade_modal_{}_{}_symbol'.format(direction, get_symbol_name(resource)),
        position=[2*x_pos/3, 2*y_pos/3],
        additional_arguments={"transform": "scale(1.5 1.5)"}
    )
    svg.create_text(
        'trade_modal_{}_{}_amount'.format(direction, resource),
        [x_pos + 15, y_pos + 40 + 14],
        "0",
        font_size=14
    )
    svg.create_circle(
        [x_pos - 10, y_pos + 40 + 7],
        8,
        'trade_modal_{}_{}_plus_circle'.format(direction, resource),
        fill_colour="#AAA",
        additional_arguments={
            "onclick": "change_{}_resource({}, 1)".format(direction, resource)
        }
    )
    svg.create_text(
        'trade_modal_{}_{}_plus'.format(direction, resource),
        [x_pos - 10, y_pos + 40 + 14],
        "+",
        font_size=14
    )
    svg.create_circle(
        [x_pos + 40, y_pos + 40 + 7],
        8,
        'trade_modal_{}_{}_minus_circle'.format(direction, resource),
        fill_colour="#AAA",
        additional_arguments={
            "onclick": "change_{}_resource({}, -1)".format(direction, resource)
        }
    )
    svg.create_text(
        'trade_modal_{}_{}_minus'.format(direction, resource),
        [x_pos + 40, y_pos + 40 + 14],
        "-",
        font_size=14
    )

def draw_trade_modal(players, planets):
    """
    draw the trading board
    """

    active_player = move.get_active_player(players)
    if active_player is None:
        return ""

    svg = Svg(width=400, height=400, id_name="trade_svg")
    add_symbols(svg)
    current_planet = None
    for planet in planets:
        if active_player.ship_position == planet.position_of_hexes[planet.current_position]:
            current_planet = planet
            break
    
    if current_planet is None:
        return "Can't trade in middle of space."
    
    svg.create_text(
        "modal_sell",
        [0, 14],
        "Sell:",
        text_anchor="start",
        font_size=14
    )
    for index, resource in enumerate(current_planet.sell_resources):
        if resource != '0':
            x_pos = 20 + index*90
            y_pos = 30
            draw_resource(svg, [x_pos, y_pos], resource, "sell")
    
    svg.create_text(
        "modal_buy",
        [0, 14 + 100],
        "Buy:",
        text_anchor="start",
        font_size=14
    )
    for index, resource in enumerate(current_planet.buy_resources):
        if resource != '0':
            x_pos = 20 + index*90
            y_pos = 130
            draw_resource(svg, [x_pos, y_pos], resource, "buy")
    
    svg.create_text(
        "modal_influence",
        [0, 14 + 200],
        "Buy Influence:",
        text_anchor="start",
        font_size=14
    )

    x_pos = 20
    y_pos = 230
    svg.create_text(
        'trade_modal_influence_amount',
        [x_pos + 15, y_pos + 40 + 14],
        "0",
        font_size=14
    )
    svg.create_circle(
        [x_pos - 10, y_pos + 40 + 7],
        8,
        'trade_modal_influence_plus_circle',
        fill_colour="#AAA",
        additional_arguments={
            "onclick": "changeInfluence(1)"
        }
    )
    svg.create_text(
        'trade_modal_influence_plus',
        [x_pos - 10, y_pos + 40 + 14],
        "+",
        font_size=14
    )
    svg.create_circle(
        [x_pos + 40, y_pos + 40 + 7],
        8,
        'trade_modal_influence_minus_circle',
        fill_colour="#AAA",
        additional_arguments={
            "onclick": "changeInfluence(-1)"
        }
    )
    svg.create_text(
        'trade_modal_influence_minus',
        [x_pos + 40, y_pos + 40 + 14],
        "-",
        font_size=14
    )

    svg_string = svg.get_string()

    return svg_string

if __name__ == '__main__':
    pass
