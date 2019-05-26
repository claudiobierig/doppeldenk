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


def draw_planet(svg, planet, name, fill_colour):
    """
    actually draw the planet market
    """
    x_shift = 30
    y_shift = [0, 30, 80]
    x_offset = [1.5*x_shift, 1.5*x_shift, x_shift/2]
    y_offset = 30
    scale_factor = 3/2
    font_size_price = 12
    font_size_header = 11

    left = x_offset[2]/2
    right = 1.5*x_offset[2] + 7*x_shift
    top = y_offset - 10
    bottom = y_offset + y_shift[1] + y_shift[2] + 10
    vertical_middle = y_offset + y_shift[1] + (y_shift[1]-y_shift[0]) + \
        (y_shift[2] - (2*y_shift[1]-y_shift[0]))/2
    horizontal_middle = 120

    svg.create_path(
        (
            "M {left},{top} V {bottom} " +
            "C {left_2},{bottom_2} {right_2},{bottom_2} {right},{bottom} " +
            "V {top} C {right_2},{top_2} {left_2},{top_2} {left},{top}").format(
                left=left, right=right, top=top, bottom=bottom,
                left_2=left+20, right_2=right-20, bottom_2=bottom+20, top_2=top-20
            ),
        stroke_colour="black",
        fill_colour=fill_colour,
        id_name="box_{}".format(name)
    )
    #svg.create_path("M {left},{middle} H {right}".format(left=left, middle=middle, right=right), stroke_colour="black")
    for i in range(1, 8):
        svg.create_text(
            "{}_pricetext_{}".format(name, i),
            [x_offset[2] + (i-0.5)*x_shift, vertical_middle + font_size_price/2],
            str(i),
            font_size=font_size_price,
            text_align="center",
            text_anchor="middle",
            font_weight="bold"
        )

    size_ellipse = [80, 10]
    offset_border_ellipse = 9
    svg.create_ellipse(
        size_ellipse,
        [horizontal_middle, top - offset_border_ellipse],
        "black",
        "ellipse_top_{}".format(name),
        fill="white",
        stroke_width="1",
        stroke_opacity="1",
        opacity="1"
    )
    svg.create_text(
        "demand_text_{}".format(name),
        [horizontal_middle, top - offset_border_ellipse + font_size_header/2],
        "Demand",
        font_size=font_size_header,
        text_align="center",
        text_anchor="middle",
        font_weight="bold"
    )

    svg.create_ellipse(
        size_ellipse,
        [horizontal_middle, bottom + offset_border_ellipse],
        "black",
        "ellipse_bottom_{}".format(name),
        fill="white",
        stroke_width="1",
        stroke_opacity="1",
        opacity="1"
    )
    svg.create_text(
        "supply_text_{}".format(name),
        [horizontal_middle, bottom + offset_border_ellipse + font_size_header/2],
        "Supply",
        font_size=font_size_header,
        text_align="center",
        text_anchor="middle",
        font_weight="bold"
    )

    resources = [planet.sell_resources[1], planet.sell_resources[0], planet.buy_resources[0]]
    prices = [planet.cost_sell_resource[1], planet.cost_sell_resource[0], planet.cost_buy_resource[0]]
    for row in range(3):
        for column in range(6):
            if row is 2:
                price = column + 1
            else:
                price = column + 2
            
            if price is prices[row]:
                symbolname = get_symbol_name(resources[row])
            else:
                symbolname = get_symbol_name('0')
            svg.use_symbol(
                symbolname,
                "{}_name_{}_row_{}_column".format(name, row, column),
                position=[(x_offset[row] + column*x_shift)/scale_factor,
                          (y_offset + y_shift[row])/scale_factor],
                additional_arguments={
                    "transform": f"scale({scale_factor})"
                }
            )


def draw_planet_market(planets):
    svgs = []
    for planet in planets:
        svg = Svg(width=240, height=170,
                  id_name="svg_planet_market_{}".format(planet.name))
        generate_svg_symbols.add_posibility_for_disc_3d(svg)
        generate_svg_symbols.add_posibility_for_empty_res(svg)
        generate_svg_symbols.add_posibility_for_red_cross(svg)
        generate_svg_symbols.add_posibility_for_radioactive(svg)
        generate_svg_symbols.add_posibility_for_food(svg)
        generate_svg_symbols.add_posibility_for_water(svg)
        generate_svg_symbols.add_posibility_for_building_res(svg)
        draw_planet(svg, planet, 'planet_market_{}'.format(planet.name), planet.colour)
        svgs.append(svg)

    return svgs


if __name__ == '__main__':
    pass
