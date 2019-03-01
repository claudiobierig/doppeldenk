#!/usr/bin/env python
"""
generate svg symbols
"""
import math
from lxml import etree

from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg.svg_commands import json_to_style


def add_posibility_for_square_3d(svg):
    """
    Create a symbol, which represents a 3d square and return it
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'square_3d',
                'view_box': '0 0 30 15'
            }
        )
    )
    width = 21
    height = 5
    depthx = 5
    depthy = 4
    left = 3
    top = 7
    symbol.create_rectangle((left, top), (width, height), "front", stroke_colour="black")
    symbol.create_polygon("{},{} {},{} {},{} {},{}".format(
            left, top,
            left + width, top,
            left + width + depthx, top - depthy,
            left + depthx, top - depthy
        ),
        stroke_colour="black"
    )
    symbol.create_polygon("{},{} {},{} {},{} {},{}".format(
            left + width, top,
            left + width + depthx, top - depthy,
            left + width + depthx, top - depthy + height,
            left + width, top + height
        ),
        stroke_colour="black"
    )
    return symbol

def add_posibility_for_disc_3d(svg):
    """
    Create a symbol, which represents a 3d disc in root and return it
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'disc_3d',
                'view_box': '0 0 30 15'
            }
        )
    )
    symbol.create_ellipse((12, 4), (15, 9), "#000000",
                          "bottom", stroke_opacity="1")
    symbol.create_rectangle((3, 5), (24, 4), "middle")
    symbol.create_ellipse((12, 4), (15, 5), "#000000",
                          "top", stroke_opacity="1")
    linestyle = {
        'stroke': '#000000',
        'stroke-width': '1',
    }
    etree.SubElement(symbol.root, 'line',
                     {
                         'x1': "3",
                         'x2': "3",
                         'y1': "5",
                         'y2': "9",
                         'style': json_to_style(linestyle),
                     }
                    )
    etree.SubElement(symbol.root, 'line',
                     {
                         'x1': "27",
                         'x2': "27",
                         'y1': "5",
                         'y2': "9",
                         'style': json_to_style(linestyle),
                     })
    return symbol

def add_posibility_for_planet_market(svg):
    """
    add a symbol for the planet market
    """
    symbol = Svg(etree.SubElement(svg.root,
                                  'symbol',
                                  {'id': 'planet_market',
                                   'view_box': '0 0 160 100'
                                  }))
    symbol.create_rectangle([0, 0], [160, 20], "top_of_planet_market")
    symbol.create_rectangle([0, 80], [160, 20], "bottom_of_planet_market")
    symbol.create_rectangle([19, 20], [2, 60], "0_sep_of_planet_market", fill_colour="black")
    symbol.create_rectangle([39, 20], [2, 60], "1st_sep_of_planet_market", fill_colour="black")
    symbol.create_rectangle([59, 20], [2, 60], "2nd_sep_of_planet_market", fill_colour="black")
    symbol.create_rectangle([79, 20], [2, 60], "3rd_sep_of_planet_market", fill_colour="black")
    symbol.create_rectangle([99, 20], [2, 60], "4th_sep_of_planet_market", fill_colour="black")
    symbol.create_rectangle([119, 20], [2, 60], "5th_sep_of_planet_market", fill_colour="black")
    symbol.create_rectangle([139, 20], [2, 60], "7th_sep_of_planet_market", fill_colour="black")
    symbol.create_rectangle([0, 0], [20, 100], "left_of_planet_market")
    symbol.create_rectangle([140, 0], [20, 100], "right_of_planet_market")
    symbol.create_rectangle([0, 45], [160, 10], "middle_of_planet_market")

    buy_values = [1, 2, 3, 4, 5, 6]
    sell_values = [7, 6, 5, 4, 3, 2]
    font_size = 12
    for index, value in enumerate(sell_values):
        symbol.create_text(
            'sell_value_{}'.format(value),
            [(index + 1.5) * 20, 16],
            str(value),
            font_size=font_size,
            font_colour="black"
        )
    
    for index, value in enumerate(buy_values):
        symbol.create_text(
            'buy_value_{}'.format(value),
            [(index + 1.5) * 20, 96],
            str(value),
            font_size=font_size,
            font_colour="black"
        )


def add_posibility_for_wheel(
        svg,
        size,
        radius,
        colour_1,
        colour_2,
        values_1,
        values_2):
    """
    Create a symbol, which represents the foreground of the resource wheel
    <path d="M160,100 A1,1 0 0,1 160,220" stroke="#FFFFFF" fill="#FFFFFF" />
    <polygon points="160,-10 160,330 180,160" style="fill:#FFFFFF" />
    <path d="M160,100 A1,1 0 0,0 160,220" stroke="#000000" fill="#000000" />
    <polygon points="160,-10 160,330 140,160" style="fill:#000000" />
    """
    symbol = Svg(etree.SubElement(svg.root,
                                  'symbol',
                                  {'id': 'foreground_symbol',
                                   'view_box': '0 0' + str(size) + ' ' + str(size)
                                  }))
    symbol.create_path("M{},{} A1,1 0 0,1 {},{}".format(size / 2,
                                                        size / 2 - radius,
                                                        size / 2,
                                                        size / 2 + radius),
                       colour_1, colour_1)
    symbol.create_polygon("{},{} {},{} {},{}".format(size / 2, -10,
                                                     size / 2, size + 10,
                                                     size / 2 + 20, size / 2),
                          colour_1)
    symbol.create_path("M{},{} A1,1 0 0,0 {},{}".format(size / 2,
                                                        size / 2 - radius,
                                                        size / 2,
                                                        size / 2 + radius),
                       colour_2, colour_2)
    symbol.create_polygon("{},{} {},{} {},{}".format(size / 2, -10,
                                                     size / 2, size + 10,
                                                     size / 2 - 20, size / 2),
                          colour_2)

    number_of_segments = len(values_1) + len(values_2)
    degrees = list(range(0, number_of_segments))
    degrees[:] = [2 * x * math.pi / number_of_segments for x in degrees]
    positions = [(radius * math.cos(x) + size / 2,
                  radius * math.sin(x) + size / 2)
                 for x in degrees]
    for position in positions:
        symbol.create_line([size / 2, size / 2], position)

    font_size = 8
    padding_numbers = 10
    radius_numbers = radius - padding_numbers
    number_of_segments_1 = len(values_1)
    degrees_1 = list(range(0, number_of_segments_1))
    degrees_1[:] = [- math.pi / 2 + (2 * x + 1) * math.pi / number_of_segments
                    for x in degrees_1]
    position_numbers_1 = [
        (radius_numbers * math.cos(x) + size / 2,
         radius_numbers * math.sin(x) + size / 2 + font_size / 2)
        for x in degrees_1
    ]
    for index, position in enumerate(position_numbers_1):
        symbol.create_text(
            "wheel_1_" + str(values_1[index]), position, str(values_1[index]),
            font_size=font_size, font_colour=colour_2
        )

    number_of_segments_2 = len(values_2)
    degrees_2 = list(reversed(range(0, number_of_segments_2)))
    degrees_2[:] = [math.pi / 2 + (2 * x + 1) * math.pi / number_of_segments
                    for x in degrees_2]

    position_numbers_2 = [
        (radius_numbers * math.cos(x) + size / 2,
         radius_numbers * math.sin(x) + size / 2 + font_size / 2)
        for x in degrees_2
    ]

    for index, position in enumerate(position_numbers_2):
        symbol.create_text(
            "wheel_2_" + str(values_2[index]), position, str(values_2[index]),
            font_size=font_size, font_colour=colour_1
        )

    return symbol


def add_posibility_for_empty_res(svg):
    """add a symbol which represents a place holder for a resource
    Arguments:
        svg {Svg} -- root element
    """
    symbol = Svg(etree.SubElement(svg.root,
                                  'symbol',
                                  {'id': 'resource_placeholder',
                                   'view_box': '0 0 20 20'
                                  }))
    symbol.create_circle(
        [10, 10],
        8,
        "resource_placeholder_circle",
        fill_colour="white",
        additional_arguments={'stroke': 'black'}
    )
    return symbol

def add_posibility_for_coin(svg):
    """add a symbol for a coin

    Arguments:
        svg {Svg} -- root svg
    """
    symbol = Svg(etree.SubElement(svg.root,
                                  'symbol',
                                  {'id': 'coin',
                                   'view_box': '0 0 20 20'
                                  }))
    subgroup = symbol.create_subgroup(
        "coin_subgroup",
        additional_arguments={
            "transform": "matrix(0.03515652,0,0,0.03515652,1,1)"
        }
    )
    subgroup.create_circle(
        [256, 256],
        256,
        "coin_outer_circle",
        fill_colour="#ffc843"
    )
    subgroup.create_circle(
        [256, 256],
        208,
        "coin_inner_circle",
        fill_colour="#d49000"
    )
    subgroup.create_path(
        "m 259.203,102.361 c 10.266,0 18.408,8.142 18.408,18.408 l 0,4.956 "
        "c 19.117,2.832 36.108,8.496 51.33,16.993 6.726,3.893 12.745,10.62 "
        "12.745,21.241 0,13.452 -10.621,23.718 -24.073,23.718 -4.247,0 -8.496,"
        "-1.062 -12.39,-3.186 -9.912,-5.31 -19.825,-9.558 -29.383,-12.036 "
        "l 0,53.81 c 53.809,14.513 76.82,36.462 76.82,76.111 0,39.649 -30.444,65.137 -75.05,70.092 "
        "l 0,18.762 c 0,10.266 -8.142,18.409 -18.408,18.409 "
        "-10.266,0 -18.408,-8.143 -18.408,-18.409 "
        "l 0,-19.116 c -25.134,-3.186 -48.854,-12.036 -69.74,-24.781 -7.434,-4.601 -12.036,-11.681 "
        "-12.036,-21.24 0,-13.806 10.621,-24.073 24.427,-24.073 4.602,0 9.558,1.77 13.807,4.602 "
        "14.868,9.558 29.029,16.285 45.313,19.825 l 0,-56.288 c -50.978,-13.806 "
        "-76.112,-33.276 -76.112,-75.403 0,-38.941 29.737,-65.137 74.342,-69.74 "
        "l 0,-4.248 c 0,-10.265 8.142,-18.407 18.408,-18.407 z m -16.637,114.698 "
        "0,-47.791 c -16.993,2.479 -24.427,10.975 -24.427,22.303 0,10.974 4.956,"
        "18.408 24.427,25.488 z m 33.276,61.952 0,49.207 c 16.639,-2.478 25.134,"
        "-10.266 25.134,-23.011 10e-4,-11.682 -6.017,-19.471 -25.134,-26.196 z",
        fill_colour="#ffc843"
    )

def add_posibility_for_red_cross(svg):
    """add a symbol which represents a red cross in a white circle
    Arguments:
        svg {Svg} -- root element
    """
    symbol = Svg(etree.SubElement(svg.root,
                                  'symbol',
                                  {'id': 'red_cross',
                                   'view_box': '0 0 20 20'
                                  }))
    symbol.create_circle(
        [10, 10],
        8,
        "red_cross_circle",
        fill_colour="white",
        additional_arguments={'stroke': 'black'}
    )
    symbol.create_rectangle(
        [4, 8], [12, 4], "red_cross_rect_1", fill_colour="red")
    symbol.create_rectangle(
        [8, 4], [4, 12], "red_cross_rect_2", fill_colour="red")
    return symbol


def add_posibility_for_radioactive(svg):
    """Create radioactive symbol
    Arguments:
        svg {Svg} -- root svg
    """
    symbol = Svg(etree.SubElement(svg.root,
                                  'symbol',
                                  {'id': 'radioactive',
                                   'view_box': '0 0 20 20'
                                  }))
    symbol.create_circle(
        [10, 10],
        9,
        "radio_active_outer_circle",
        additional_arguments={
            "stroke": "black"
        }
    )
    subgroup = symbol.create_subgroup(
        "radioactive_subgroup",
        additional_arguments={
            "style": "fill:#f1cd43",
            "transform": "matrix(0.03012449,0,0,0.03012449,10.00001,9.99998)"
        }
    )
    subgroup.create_circle([0, 0], 50, "radio_active_inner_circle")
    subgroup.create_path(
        "M 75,0 A 75,75 0 0 0 37.5,-64.951905 L 125,-216.50635 A 250,250 0 0 1 250,0 Z",
        "#f1cd43",
        "#f1cd43",
        "nuclear_third")
    subgroup.use_symbol(
        "nuclear_third", "nuclear_third_2", None,
        additional_arguments={
            'transform': "matrix(-0.5,0.8660254,-0.8660254,-0.5,0,0)"
        }
    )
    subgroup.use_symbol(
        "nuclear_third", "nuclear_third_3", None,
        additional_arguments={
            'transform': "matrix(-0.5,-0.8660254,0.8660254,-0.5,0,0)"
        }
    )
    return symbol


def add_posibility_for_food(svg):
    """
    Create food symbol

    Arguments:
        svg {Svg} -- root svg element
    """
    stroke_colour = "black"  # "#FFD700"
    fill_colour = "#FFD700"
    symbol = Svg(etree.SubElement(svg.root,
                                  'symbol',
                                  {'id': 'food',
                                   'view_box': '0 0 20 20'
                                  }))
    symbol.create_circle(
        [10, 10],
        9,
        "food_background_circle",
        fill_colour="#CCC",
        additional_arguments={
            "stroke": "black"
        }
    )
    subgroup = symbol.create_subgroup(
        "food_subgroup",
        additional_arguments={
            "transform": "matrix(0.18490611,0,0,0.18490611,5.0000462,5.0283833)"
        }
    )
    pathes = [
        "m 39.053,17.527"
        "c 2.694,-0.428 4.773,-2.507 5.201,-5.201"
        "l 0.994,-3.598 -3.597,0.994"
        "c -2.694,0.428 -4.773,2.507 -5.202,5.201"
        "L 36.014,16.5"
        "c 0,0 -0.001,0 -0.001,0"
        "L 0.293,52.221"
        "c -0.391,0.391 -0.391,1.023 0,1.414 0.195,0.195 0.451,"
        "0.293 0.707,0.293 0.256,0 0.512,-0.098 0.707,-0.293"
        "L 37.342,18 39.053,17.527 Z",
        "m 32.529,19.183 1.841,-3.245 c 1.602,-2.208 1.603,-5.149 0,-7.356"
        "L 32.529,5.335 30.688,8.582 c -1.603,2.207 -1.603,5.147 0,7.356 l 1.841,3.245 z",
        "m 37.991,19.559 -3.246,1.841 3.246,1.841"
        "c 1.076,0.781 2.347,1.193 3.678,1.193 1.331,0 2.602,-0.412 3.678,-1.193"
        "L 48.594,21.4 45.347,19.559 c -2.153,-1.563 -5.204,-1.563 -7.356,0 z",
        "m 26.165,25.548 1.841,-3.247 c 1.603,-2.208 1.603,-5.147 0,-7.355"
        "l -1.841,-3.247 -1.841,3.247 c -1.602,2.208 -1.602,5.147 0,7.355 l 1.841,3.247 z",
        "m 31.627,25.922 -3.246,1.841 3.246,1.841"
        "c 1.076,0.781 2.346,1.194 3.678,1.194 1.332,0 2.602,-0.413 3.678,-1.194"
        "l 3.245,-1.841 -3.245,-1.841 c -2.152,-1.563 -5.204,-1.563 -7.356,0 z",
        "m 19.801,31.912 1.841,-3.247 c 1.602,-2.207 1.602,-5.147 0,-7.356"
        "l -1.841,-3.245 -1.841,3.245 c -1.603,2.209 -1.603,5.149 0,7.356 l 1.841,3.247 z",
        "m 25.263,32.286 -3.246,1.841 3.246,1.841"
        "c 1.076,0.781 2.347,1.193 3.678,1.193 1.331,0 2.602,"
        "-0.412 3.678,-1.193 l 3.246,-1.841 -3.246,-1.841"
        "c -2.152,-1.562 -5.203,-1.561 -7.356,0 z",
        "m 13.437,38.274 1.841,-3.245 c 1.603,-2.208 1.603,-5.148 0,-7.356"
        "l -1.841,-3.245 -1.841,3.245 c -1.602,2.208 -1.602,5.148 0,7.356 l 1.841,3.245 z",
        "m 18.899,38.65 -3.246,1.841 3.246,1.841 "
        "c 1.076,0.781 2.347,1.193 3.678,1.193 1.331,0 2.602,-0.412 3.678,-1.193"
        "l 3.246,-1.841 -3.246,-1.841 c -2.152,-1.562 -5.204,-1.562 -7.356,0 z",
        "m 7.073,44.64 1.841,-3.247 c 1.603,-2.208 1.603,-5.147 0,-7.355"
        "L 7.073,30.79 5.232,34.037 c -1.603,2.208 -1.603,5.147 0,7.355 l 1.841,3.248 z",
        "m 12.535,45.014 -3.246,1.841 3.246,1.841"
        "c 1.076,0.781 2.346,1.194 3.678,1.194 1.332,0 2.602,-0.413 3.678,-1.194"
        "l 3.246,-1.841 -3.246,-1.841 c -2.152,-1.562 -5.203,-1.562 -7.356,0 z",
        "m 36.11,7.811 c 0.256,0 0.512,-0.098 0.707,-0.293 l 5.657,-5.657"
        "c 0.391,-0.391 0.391,-1.023 0,-1.414 -0.391,-0.391 -1.023,-0.391 -1.414,0 l -5.657,5.657"
        "c -0.391,0.391 -0.391,1.023 0,1.414 0.196,0.195 0.451,0.293 0.707,0.293 z",
        "m 39.646,8.932 c 0.195,0.195 0.451,0.293 0.707,0.293 0.256,0 0.512,-0.098 0.707,-0.293"
        "l 7.071,-7.071 c 0.391,-0.391 0.391,-1.023 0,-1.414 -0.391,-0.391 -1.023,-0.391 -1.414,0"
        "l -7.071,7.071 c -0.391,0.39 -0.391,1.023 0,1.414 z",
        "m 52.374,6.104 -7.071,7.071"
        "c -0.391,0.391 -0.391,1.023 0,1.414 0.195,0.195 0.451,"
        "0.293 0.707,0.293 0.256,0 0.512,-0.098 0.707,-0.293"
        "l 7.071,-7.071 c 0.391,-0.391 0.391,-1.023 0,"
        "-1.414 -0.391,-0.391 -1.023,-0.391 -1.414,0 z",
        "m 46.01,8.225 c 0.195,0.195 0.451,0.293 0.707,0.293 0.256,0 0.512,-0.098 0.707,-0.293"
        "l 6.364,-6.364 c 0.391,-0.391 0.391,-1.023 0,-1.414 -0.391,-0.391 -1.023,-0.391 -1.414,0"
        "L 46.01,6.811 c -0.391,0.39 -0.391,1.023 0,1.414 z",
        "m 52.374,11.761 -5.657,5.656"
        "c -0.391,0.391 -0.391,1.023 0,1.414 0.195,"
        "0.195 0.451,0.293 0.707,0.293 0.256,0 0.512,-0.098 0.707,-0.293"
        "l 5.657,-5.656 c 0.391,-0.391 0.391,-1.023 0,"
        "-1.414 -0.391,-0.391 -1.023,-0.391 -1.414,0 z"
    ]
    for index, path in enumerate(pathes):
        subgroup.create_path(
            path,
            stroke_colour,
            fill_colour,
            id_name="food_path_{}".format(index)
        )
    return symbol

def add_posibility_for_water(svg):
    """
    Create water symbol

    Arguments:
        svg {Svg} -- root svg element
    """

    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'water',
                'view_box': '0 0 20 20'
            }
        )
    )
    symbol.create_circle(
        [10, 10],
        9,
        "water_background_circle",
        fill_colour="#77B3D4",
        additional_arguments={
            "stroke": "black"
        }
    )
    subgroup = symbol.create_subgroup(
        "water_subgroup",
        additional_arguments={
            "transform": "matrix(0.28125,0,0,0.28125,1,1)"
        }
    )
    subgroup.create_path(
        "M48,37.1C48,46.4,40.8,54,32,54s-16-7.6-16-16.9S25.6,20.2,32,10C38.4,20.2,48,27.7,48,37.1z",
        id_name="water_path1",
        fill_colour="#231F20",
        additional_arguments={
            "opacity" : "0.2"
        }
    )
    subgroup.create_path(
        "M48,35.1C48,44.4,40.8,52,32,52s-16-7.6-16-16.9S25.6,18.2,32,8C38.4,18.2,48,25.7,48,35.1z",
        id_name="water_path2",
        fill_colour="#FFFFFF"
    )

def add_posibility_for_building_res(svg):
    """
    Add building resource symbol

    Arguments:
        svg {Svg} -- root svg element
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'building_resource',
                'view_box': '0 0 20 20'
            }
        )
    )
    symbol.create_circle(
        [10, 10],
        9,
        "building_resource_background_circle",
        fill_colour="#B22222",
        additional_arguments={
            "stroke": "black"
        }
    )
    symbol.create_path(
        "m 16.9923,6.2679064 c -7e-4,-0.0028 -0.0024,"
        "-0.00514 -0.0032,-0.00794 -0.0052,-0.0168 "
        "-0.01144,-0.033134 -0.02006,-0.0483 -0.0035,"
        "-0.0063 -0.0087,-0.011434 -0.01284,-0.0175 "
        "-0.0074,-0.010497 -0.0147,-0.02123 -0.0238,"
        "-0.030564 -0.006,-0.00607 -0.0133,-0.010967 "
        "-0.02006,-0.016333 -0.0074,-0.00606 -0.01424,"
        "-0.013066 -0.02264,-0.018434 -0.0018,-0.00116 "
        "-0.0042,-0.00164 -0.006,-0.0028 -0.0018,-0.00116 "
        "-0.0032,-0.0028 -0.0053,-0.00396 l -4.2,-2.2938999 "
        "c -0.06814,-0.037102 -0.1498,-0.038269 -0.218866,"
        "-0.00257 L 3.126,8.6425397 c -0.00326,0.00164 "
        "-0.0056,0.00444 -0.00864,0.0063 -0.00374,0.0021 "
        "-0.00816,0.00326 -0.0119,0.00584 -0.007,0.00466 "
        "-0.0126,0.010734 -0.0189,0.0161 -0.0063,0.00514 "
        "-0.012834,0.010034 -0.018666,0.015866 -0.00933,0.00933 "
        "-0.017034,0.019834 -0.0245,0.030566 -0.00396,0.00606 "
        "-0.00864,0.011434 -0.012366,0.017734 -0.00794,0.014 "
        "-0.013766,0.028934 -0.018666,0.044334 -0.0014,0.0042 "
        "-0.0035,0.0077 -0.00466,0.0119 C 3.0028,8.8103064 "
        "3,8.8301397 3,8.8502064 l 0,3.8994666 c 0,0.09147 "
        "0.053434,0.174533 0.1367334,0.212333 l 4.4333332,"
        "2.016934 c 0.0035,0.0017 0.00746,9.62e-4 0.010966,"
        "0.0024 C 7.6085666,14.99254 7.6372666,15 7.6666666,15 "
        "c 0.020534,0 0.040834,-0.0032 0.060666,-0.0087 "
        "0.00654,-0.0018 0.012366,-0.0049 0.0189,-0.0073 "
        "0.00957,-0.0035 0.0196,-0.006 0.0287,-0.01096 l "
        "9.1000014,-4.7695 C 16.951934,10.163406 17,10.08384 "
        "17,9.9970398 l 0,-3.6698667 c 0,-0.0203 -0.0025,"
        "-0.040134 -0.0077,-0.059266 z m -4.4289,-1.9705 "
        "3.696234,2.0188 -8.5985674,4.2263666 -3.8864,-1.7091666"
        " 8.7887334,-4.536 z m -9.0967334,4.9179667 "
        "3.9666668,1.8370329 0,3.351834 -3.9666668,-1.804834 "
        "0,-3.3840329 z M 7.9,14.380906 l 0,-3.3103 8.633334,"
        "-4.3640329 0,3.1493 L 7.9,14.380906 Z",
        fill_colour="#AAA"
    )

def main():
    """
    no main implemented
    """
    print("no main implemented")


if __name__ == '__main__':
    main()
