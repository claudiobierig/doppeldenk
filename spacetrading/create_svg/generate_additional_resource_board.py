#!/usr/bin/env python
"""
generate influence tracks
"""
from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg import generate_svg_symbols


def draw_additional_resource_board(game, planets):
    """
    draw board where additional resources are displayed
    """
    width = 40
    height = 80
    svg = Svg(
        width=str(len(planets)*width),
        height=str(height),
        id_name="additional_resource_board"
    )

    generate_svg_symbols.add_posibility_for_empty_res(svg)
    generate_svg_symbols.add_posibility_for_red_cross(svg)
    generate_svg_symbols.add_posibility_for_radioactive(svg)
    generate_svg_symbols.add_posibility_for_food(svg)
    generate_svg_symbols.add_posibility_for_water(svg)
    generate_svg_symbols.add_posibility_for_building_res(svg)
    sorted_planets = sorted(planets, key=lambda planet: planet.add_demand_resource_time)
    for index, planet in enumerate(sorted_planets):
        if game.add_demand_event_time <= planet.add_demand_resource_time:
            svg.create_rectangle(
                [width*index, 0],
                [width, height],
                f"add_demand_resource_planet_{planet.name}_rectangle",
                fill_colour=planet.colour,
                stroke_width="2",
                stroke_colour="black"
            )
            scale_factor = 3/2
            svg.use_symbol(
                generate_svg_symbols.get_symbol_name(planet.add_demand_resource),
                f"add_demand_resource_planet_{planet.name}_resource",
                position=[(width*index + 5)/scale_factor, 5/scale_factor],
                additional_arguments={
                    "transform": f"scale({scale_factor})"
                }
            )
            svg.use_symbol(
                'resource_placeholder',
                f"add_demand_resource_planet_{planet.name}_empty",
                position=[(width*index + 5)/scale_factor, 45/scale_factor],
                additional_arguments={
                    "transform": f"scale({scale_factor})"
                }
            )
            font_size = 12
            svg.create_text(
                f"add_demand_resource_planet_{planet.name}_text",
                [width*index + 20, 60 + font_size/2],
                str(planet.add_demand_resource_price),
                font_size=font_size,
                text_align="center",
                text_anchor="middle",
                font_weight="bold"
            )

    svg_string = svg.get_string()
    return svg_string

if __name__ == '__main__':
    pass