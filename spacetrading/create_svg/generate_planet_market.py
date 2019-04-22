#!/usr/bin/env python
"""
generate the planet market
"""

from spacetrading.create_svg.svg_commands import Svg, get_position
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
    x_pos = 30 * price + 30
    y_pos = 112
    return [x_pos, y_pos]

def get_rel_sell_position(price):
    x_pos = 270 - (30*price)
    y_pos = 67
    return [x_pos, y_pos]

def draw_planet(svg, name, fill_colour):
    """
    actually draw the planet market
    """
    svg.create_rectangle([30, 30], [240, 35], "top_of_planet_market_{}".format(name), fill_colour=fill_colour)
    svg.create_rectangle([30, 145], [240, 35], "bottom_of_planet_market_{}".format(name), fill_colour=fill_colour)
    svg.create_rectangle([59, 65], [2, 80], "0_sep_of_planet_market_{}".format(name), fill_colour="black")
    svg.create_rectangle([89, 65], [2, 80], "1st_sep_of_planet_market_{}".format(name), fill_colour="black")
    svg.create_rectangle([119, 65], [2, 80], "2nd_sep_of_planet_market_{}".format(name), fill_colour="black")
    svg.create_rectangle([149, 65], [2, 80], "3rd_sep_of_planet_market_{}".format(name), fill_colour="black")
    svg.create_rectangle([179, 65], [2, 80], "4th_sep_of_planet_market_{}".format(name), fill_colour="black")
    svg.create_rectangle([209, 65], [2, 80], "5th_sep_of_planet_market_{}".format(name), fill_colour="black")
    svg.create_rectangle([239, 65], [2, 80], "7th_sep_of_planet_market_{}".format(name), fill_colour="black")
    svg.create_rectangle([30, 30], [30, 150], "left_of_planet_market_{}".format(name), fill_colour=fill_colour)
    svg.create_rectangle([240, 30], [30, 150], "right_of_planet_market_{}".format(name), fill_colour=fill_colour)
    svg.create_rectangle([30, 100], [240, 10], "middle_of_planet_market_{}".format(name), fill_colour=fill_colour)

    buy_values = [1, 2, 3, 4, 5, 6]
    sell_values = [7, 6, 5, 4, 3, 2]
    font_size = 12
    for index, value in enumerate(sell_values):
        svg.create_text(
            'sell_value_{}_{}'.format(name, value),
            [index * 30 + 75, 56],
            str(value),
            font_size=font_size,
            font_colour="black"
        )
    
    for index, value in enumerate(buy_values):
        svg.create_text(
            'buy_value_{}_{}'.format(name, value),
            [index * 30 + 75, 166],
            str(value),
            font_size=font_size,
            font_colour="black"
        )

    svg.create_scoring_track(
        30,
        "influence_track_{}".format(name),
        9,
        6,
        5,
        fill_colour=fill_colour
    )


def draw_influence_tokens(svg, points, players, planetname):
    planet_points = []
    for player in players:
        player_points = points[player.player_number]
        stack_position = planet_points.count(player_points)
        planet_points.append(player_points)
        position = get_position(30, 9, 6, player_points, stack_position)
        svg.use_symbol(
            'disc_3d',
            'influence_marker_{}_{}'.format(player.user.get_username(), planetname),
            position=position,
            fill_colour=player.colour
        )

def draw_planet_market(game, planets, players):
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
        draw_influence_tokens(svg, game.planet_influence_track[planet_number], players, planet.name)

        for price, resource in zip(planet.cost_buy_resource, planet.buy_resources):
            if resource is not '0':
                [x_pos, y_pos] = get_rel_buy_position(price)
                x_pos = x_pos
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
                x_pos = x_pos
                symbol_name = get_symbol_name(resource)
                svg.use_symbol(
                    symbol_name,
                    'planet_{}_buy_resource'.format(planet.name),
                    position=[x_pos*2/3, y_pos*2/3],
                    additional_arguments={"transform": "scale(1.5)"}
                )
        svgs.append(svg.get_string())

    return svgs

if __name__ == '__main__':
    pass
