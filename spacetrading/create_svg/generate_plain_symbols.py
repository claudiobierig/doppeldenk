#!/usr/bin/env python
"""
generate the plain symbols
"""

from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg import generate_svg_symbols

def draw_single_symbol(symbolname):
    svg = Svg(width=30, height=30, id_name="svg_{}".format(symbolname))
    if symbolname == "coin":
        generate_svg_symbols.add_posibility_for_coin(svg)
    elif symbolname == "red_cross":
        generate_svg_symbols.add_posibility_for_red_cross(svg)
    elif symbolname == "radioactive":
        generate_svg_symbols.add_posibility_for_radioactive(svg)
    elif symbolname == "food":
        generate_svg_symbols.add_posibility_for_food(svg)
    elif symbolname == "water":
        generate_svg_symbols.add_posibility_for_water(svg)
    elif symbolname == "building_resource":
        generate_svg_symbols.add_posibility_for_building_res(svg)
    elif symbolname == "influence":
        generate_svg_symbols.add_posibility_for_influence(svg)
    elif symbolname == "time":
        generate_svg_symbols.add_posibility_for_time(svg)

    svg.use_symbol(
        symbolname,
        "{}_symbol".format(symbolname),
        position=[0, 0],
        additional_arguments={"transform": "scale(1.5 1.5)"}
    )
    return svg.get_string()

def draw_symbols():
    """
    draw the symbols and return them in a json
    """
    svgs = {
        "coin": draw_single_symbol("coin"),
        "red_cross": draw_single_symbol("red_cross"),
        "radioactive": draw_single_symbol("radioactive"),
        "food": draw_single_symbol("food"),
        "water": draw_single_symbol("water"),
        "building_resource": draw_single_symbol("building_resource"),
        "influence": draw_single_symbol("influence"),
        "time": draw_single_symbol("time")
    }

    return svgs

if __name__ == '__main__':
    pass
