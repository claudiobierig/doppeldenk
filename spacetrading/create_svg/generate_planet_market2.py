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

def draw_planet(svg, name, fill_colour):
    """
    actually draw the planet market
    """

def draw_planet_market(planets):
    svgs = []
    for planet_number, planet in enumerate(planets):
        svg = Svg(width=300, height=210, id_name="svg_planet_market_{}".format(planet.name))
        generate_svg_symbols.add_posibility_for_disc_3d(svg)
        generate_svg_symbols.add_posibility_for_empty_res(svg)
        generate_svg_symbols.add_posibility_for_red_cross(svg)
        generate_svg_symbols.add_posibility_for_radioactive(svg)
        generate_svg_symbols.add_posibility_for_food(svg)
        generate_svg_symbols.add_posibility_for_water(svg)
        generate_svg_symbols.add_posibility_for_building_res(svg)
        draw_planet(svg, 'planet_market_{}'.format(planet.name), planet.colour)
        svgs.append(svg.get_string())

    return svgs

if __name__ == '__main__':
    pass
