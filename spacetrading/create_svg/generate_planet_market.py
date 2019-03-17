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

def get_rel_buy_position(price):
    x_pos = 30 * price - 10
    y_pos = 77
    return [x_pos, y_pos]

def get_rel_sell_position(price):
    x_pos = 230 - (30*price)
    y_pos = 32
    return [x_pos, y_pos]


def draw_planet_market(planets):
    svg = Svg(width=5*220, height=140, id_name="all_planet_markets")
    generate_svg_symbols.add_posibility_for_planet_market(svg)
    generate_svg_symbols.add_posibility_for_empty_res(svg)
    generate_svg_symbols.add_posibility_for_red_cross(svg)
    generate_svg_symbols.add_posibility_for_radioactive(svg)
    generate_svg_symbols.add_posibility_for_food(svg)
    generate_svg_symbols.add_posibility_for_water(svg)
    generate_svg_symbols.add_posibility_for_building_res(svg)
    for index, planet in enumerate(planets):
        x_offset = index*220
        svg.use_symbol(
            'planet_market',
            'planet_market_{}'.format(planet.name),
            position=[x_offset, 0],
            fill_colour=planet.colour
        )
        for price, resource in zip(planet.cost_buy_resource, planet.buy_resources):
            if resource is not '0':
                [x_pos, y_pos] = get_rel_buy_position(price)
                x_pos = x_pos + x_offset
                symbol_name = get_symbol_name(resource)
                svg.use_symbol(
                    symbol_name,
                    'planet_{}_buy_resource'.format(planet.name),
                    position=[x_pos*2/3, y_pos*2/3],
                    additional_arguments={"transform": "scale(1.5)"}
                )

        for price, resource in zip(planet.cost_sell_resource, planet.sell_resources):
            if resource is not '0':
                [x_pos, y_pos] = get_rel_sell_position(price)
                x_pos = x_pos + x_offset
                symbol_name = get_symbol_name(resource)
                svg.use_symbol(
                    symbol_name,
                    'planet_{}_buy_resource'.format(planet.name),
                    position=[x_pos*2/3, y_pos*2/3],
                    additional_arguments={"transform": "scale(1.5)"}
                )


    return svg.get_string()

if __name__ == '__main__':
    pass
