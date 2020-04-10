#!/usr/bin/env python
"""
generate svg symbols
"""
from lxml import etree

from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg.svg_commands import json_to_style


def get_symbol_name(resource):
    if resource == '0':
        return 'resource_placeholder'
    elif resource == '1':
        return 'red_cross'
    elif resource == '2':
        return 'radioactive'
    elif resource == '3':
        return 'food'
    elif resource == '4':
        return 'water'
    elif resource == '5':
        return 'building_resource'
    return resource


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
    depthx = 4
    depthy = 6
    left = 3
    top = 7
    symbol.create_rectangle((left, top), (width, height),
                            "front", stroke_colour="black")
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
        9,
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
        9,
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
    stroke_colour = "black"
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
        fill_colour="#008000",
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
            "opacity": "0.2"
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
        fill_colour="#FF8000",
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
        fill_colour="#000"
    )


def add_posibility_for_influence(svg):
    """
    Create influence symbol

    Arguments:
        svg {Svg} -- root svg element
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'influence',
                'view_box': '0 0 20 20'
            }
        )
    )
    background_colour = "#000"
    foreground_colour = "#AAA"
    symbol.create_circle(
        [10, 10],
        9,
        "influence_background_circle",
        fill_colour=background_colour
    )
    symbol.create_circle(
        [10, 10],
        1,
        "influence_middle",
        fill_colour=foreground_colour
    )
    symbol.create_circle(
        [10, 10],
        4,
        "influence_ring_inner",
        additional_arguments={
            "fill-opacity": "1",
            "stroke": foreground_colour,
            "stroke-dasharray": "4 1",
            "stroke-width": "1",
            "fill": "none"
        }
    )
    symbol.create_circle(
        [10, 10],
        7,
        "influence_ring_outer",
        additional_arguments={
            "fill-opacity": "1",
            "stroke": foreground_colour,
            "stroke-dasharray": "4 1",
            "stroke-width": "1",
            "fill": "none"
        }
    )


def add_posibility_for_planet_rotation(svg):
    """
    add symbol for planet rotation
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'planet_rotation',
                'view_box': '0 0 30 30'
            }
        )
    )
    symbol.create_rectangle(
        [0, 0],
        [30, 30],
        "background_planet_rotation",
        fill_colour="yellow"
    )
    symbol.create_path(
        "m 15,0 c -2.74055,0 -5.30948,0.73841 -7.52141,2.02448 -0.56742,-0.60807 -1.37452,-0.99 -2.26738,-0.99 -1.70783,0 -3.10345,1.39562 -3.10345,3.10345 0,0.77824 0.29048,1.49121 0.76758,2.03721 C 1.06821,8.65241 0,11.70217 0,15 0,23.27814 6.72186,30 15,30 23.27814,30 30,23.27814 30,15 30,6.72186 23.27814,0 15,0 Z m 0,1.03448 C 22.7191,1.03448 28.96552,7.2809 28.96552,15 28.96552,22.7191 22.7191,28.96552 15,28.96552 7.2809,28.96552 1.03448,22.7191 1.03448,15 c 0,-3.05276 0.97831,-5.874 2.63711,-8.17076 0.45444,0.26152 0.98007,0.41214 1.53962,0.41214 1.70782,0 3.10345,-1.39562 3.10345,-3.10345 0,-0.44586 -0.0957,-0.8701 -0.26669,-1.2541 C 10.09469,1.70783 12.46769,1.03448 15,1.03448 Z M 5.21121,2.06897 c 1.14879,0 2.06896,0.92017 2.06896,2.06896 0,1.14879 -0.92017,2.06897 -2.06896,2.06897 -1.1488,0 -2.06897,-0.92018 -2.06897,-2.06897 0,-1.14879 0.92017,-2.06896 2.06897,-2.06896 z M 15,4.13793 C 9.00714,4.13793 4.13793,9.00714 4.13793,15 c 0,5.99286 4.86921,10.86207 10.86207,10.86207 2.92438,0 5.58031,-1.16028 7.53434,-3.04407 0.36083,0.1919 0.77131,0.30124 1.20642,0.30124 1.42221,0 2.58621,-1.164 2.58621,-2.58621 0,-0.84082 -0.40697,-1.59113 -1.03345,-2.06431 C 25.66148,17.3791 25.86207,16.21283 25.86207,15 25.86207,9.00714 20.99286,4.13793 15,4.13793 Z m 0,1.03448 c 5.43372,0 9.82759,4.39387 9.82759,9.82759 0,1.05466 -0.16604,2.07 -0.47256,3.02183 -0.19706,-0.0485 -0.40272,-0.075 -0.61427,-0.075 -1.42221,0 -2.58621,1.164 -2.58621,2.5862 0,0.615 0.21807,1.18149 0.58004,1.62673 C 19.97659,23.814 17.60865,24.82759 15,24.82759 9.56628,24.82759 5.17241,20.43372 5.17241,15 5.17241,9.56628 9.56628,5.17241 15,5.17241 Z m 0,3.10345 c -3.70748,0 -6.72414,3.01666 -6.72414,6.72414 0,0.52055 0.0616,1.02652 0.17462,1.51314 -0.47534,0.38017 -0.78227,0.96352 -0.78227,1.61472 0,1.13648 0.93248,2.06897 2.06896,2.06897 0.28635,0 0.55976,-0.0596 0.80855,-0.16624 1.18707,1.05258 2.74687,1.69355 4.45428,1.69355 3.70748,0 6.72414,-3.01666 6.72414,-6.72414 0,-3.70748 -3.01666,-6.72414 -6.72414,-6.72414 z m 0,1.03448 c 3.14845,0 5.68966,2.54121 5.68966,5.68966 0,3.14845 -2.54121,5.68966 -5.68966,5.68966 -1.38041,0 -2.6429,-0.48973 -3.62679,-1.30387 0.27,-0.34965 0.43282,-0.78548 0.43282,-1.25793 0,-1.13658 -0.93248,-2.06896 -2.06896,-2.06896 -0.10976,0 -0.21755,0.009 -0.32286,0.0256 -0.0677,-0.351 -0.10387,-0.71338 -0.10387,-1.08455 0,-3.14845 2.54121,-5.68966 5.68966,-5.68966 z m -0.67438,2.66638 c -0.21569,10e-4 -0.4079,0.13604 -0.48248,0.33838 l -0.29276,0.79552 -0.84414,0.077 c -0.28448,0.026 -0.49417,0.27755 -0.46821,0.56213 0.005,0.0589 0.0208,0.11628 0.0455,0.16987 l 0.35566,0.76955 -0.54269,0.6512 c -0.18279,0.21952 -0.1531,0.54569 0.0665,0.72859 0.0454,0.0378 0.0969,0.0675 0.15238,0.0879 l 0.79541,0.29276 0.077,0.84414 c 0.0261,0.28448 0.27776,0.49407 0.56235,0.468 0.0588,-0.005 0.11617,-0.0208 0.16976,-0.0455 l 0.76944,-0.35534 0.65142,0.54248 c 0.21952,0.18279 0.54569,0.1531 0.72858,-0.0665 0.0378,-0.0454 0.0675,-0.0969 0.0879,-0.15238 l 0.29276,-0.79551 0.84414,-0.0768 c 0.28448,-0.0261 0.49407,-0.27776 0.468,-0.56224 -0.005,-0.0588 -0.0208,-0.11618 -0.0455,-0.16976 l -0.35545,-0.76966 0.54249,-0.65121 c 0.18279,-0.21951 0.1531,-0.54568 -0.0665,-0.72848 -0.0454,-0.0378 -0.0969,-0.0675 -0.15238,-0.0879 l -0.79542,-0.29276 -0.0768,-0.84414 c -0.026,-0.28448 -0.27765,-0.49417 -0.56214,-0.4682 -0.0589,0.005 -0.11627,0.0208 -0.16986,0.0455 l -0.76955,0.35566 -0.65121,-0.54248 c -0.094,-0.078 -0.21227,-0.12042 -0.33424,-0.1198 z m 0.23514,1.38383 0.339,0.28242 c 0.15341,0.12775 0.36672,0.15589 0.54796,0.0721 l 0.40087,-0.18507 0.04,0.43966 c 0.0181,0.19882 0.14906,0.36941 0.33641,0.43841 l 0.41421,0.15259 -0.28242,0.339 c -0.12786,0.15351 -0.15589,0.36682 -0.0721,0.54817 l 0.18507,0.40065 -0.43945,0.04 c -0.19882,0.0182 -0.36951,0.14917 -0.43841,0.33662 l -0.15259,0.4142 -0.3392,-0.28251 c -0.15342,-0.12786 -0.36662,-0.156 -0.54797,-0.0723 l -0.40086,0.18507 -0.04,-0.43945 c -0.0181,-0.19883 -0.14907,-0.36942 -0.33642,-0.43842 l -0.41441,-0.15258 0.28262,-0.33921 c 0.12776,-0.15341 0.1559,-0.36672 0.0721,-0.54796 l -0.18507,-0.40066 0.43966,-0.04 c 0.19883,-0.0182 0.36952,-0.14918 0.43841,-0.33662 z m -4.82369,3.73283 c 0.57745,0 1.03448,0.45703 1.03448,1.03448 0,0.57745 -0.45703,1.03448 -1.03448,1.03448 -0.57745,0 -1.03448,-0.45703 -1.03448,-1.03448 0,-0.57745 0.45703,-1.03448 1.03448,-1.03448 z m 14.00369,1.88793 c 0.86317,0 1.55172,0.68855 1.55172,1.55172 0,0.86318 -0.68855,1.55173 -1.55172,1.55173 -0.86317,0 -1.55173,-0.68855 -1.55173,-1.55173 0,-0.86317 0.68866,-1.55172 1.55173,-1.55172 z"  # noqa: E501
    )


def add_posibility_for_production(svg):
    """
    add symbol for production
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'production',
                'view_box': '0 0 30 30'
            }
        )
    )
    symbol.create_rectangle(
        [0, 0],
        [30, 30],
        "background_production",
        fill_colour="orange"
    )
    symbol.create_path(
        "m 30,15.430363 v 12.16492 c 0,0.40737 -0.330345,0.73771 -0.737706,0.73771 H 0.73770613 C 0.3303448,28.332993 0,28.002653 0,27.595283 v -8.60755 c 0,-0.27974 0.15816419,-0.53528 0.40839411,-0.6601 l 7.13111009,-3.55737 c 0.2286889,-0.11405 0.5001647,-0.10165 0.7173454,0.0328 0.2173282,0.13441 0.3496727,0.3718 0.3496727,0.62734 v 2.36494 L 12.9733,15.617043 V 8.4123126 c 0,-0.40736 0.330345,-0.73771 0.737706,-0.73771 h 1.338789 c 0.407361,0 0.737706,0.33035 0.737706,0.73771 v 9.3582404 l 4.871959,-2.4303 0.301574,-13.0705304 c 0.0093,-0.40072 0.336689,-0.72073 0.737559,-0.72073 h 3.215956 c 0.400722,0 0.728264,0.32001 0.737559,0.72073 l 0.322525,13.9764404 2.958349,-1.47571 c 0.228689,-0.11405 0.500017,-0.10166 0.717345,0.0327 C 29.867656,14.937573 30,15.174823 30,15.430363 Z M 5.1754511,22.362733 H 3.179956 v 2.80417 h 1.9954951 z m 5.4036969,0 H 8.5836534 v 2.80417 h 1.9954946 z m 5.403845,0 h -1.995495 v 2.80417 h 1.995495 z m 5.403845,0 h -1.995495 v 2.80417 h 1.995495 z"  # noqa: E501
    )


def add_posibility_for_time(svg):
    """
    add symbol for time
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'time',
                'view_box': '0 0 20 20'
            }
        )
    )
    subgroup = symbol.create_subgroup(
        "time_group",
        additional_arguments={
            "transform": "translate(-306.4286,-335.2193) matrix(0.55555509,0,0,0.55555509,205.31758,203.06969)"
        }
    )
    subgroup.create_path(
        "m 200,237.86949 c -9.91413,0 -18.00001,8.08588 -18.00001,18.00002 0,9.91413 8.08588,18.00001 18.00001,18.00001 9.91414,0 18.00002,-8.08588 18.00002,-18.00001 0,-9.91414 -8.08588,-18.00002 -18.00002,-18.00002 z m 0,4.00001 c 7.74989,0 14.00002,6.25013 14.00002,14.00001 0,7.74988 -6.25013,14.00001 -14.00002,14.00001 -7.74988,0 -14.00001,-6.25013 -14.00001,-14.00001 0,-7.74988 6.25013,-14.00001 14.00001,-14.00001 z"  # noqa: E501
    )
    subgroup.create_path(
        "m 200.25,242.625 c -1.10458,0.0172 -1.98603,0.92667 -1.96875,2.03125 V 258.375 c -0.009,0.73187 0.38285,1.41011 1.02113,1.76832 0.63827,0.35822 1.42123,0.33921 2.04137,-0.0496 L 208.625,255.625 c 0.63407,-0.36193 1.02057,-1.04058 1.00836,-1.77057 -0.0122,-0.72999 -0.42119,-1.39534 -1.067,-1.73586 -0.64582,-0.34053 -1.42586,-0.30213 -2.03511,0.10018 l -4.25,2.59375 v -10.15625 c 0.008,-0.54127 -0.20282,-1.06287 -0.5856,-1.44565 -0.38278,-0.38278 -0.90438,-0.59407 -1.44565,-0.5856 z"  # noqa: E501
    )


def add_posibility_for_politician(svg):
    """
    add possibility for person
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'politician',
                'view_box': '0 0 30 30'
            }
        )
    )
    subgroup = symbol.create_subgroup(
        "politician_group",
        additional_arguments={
            "transform": "matrix(0.03061224,0,0,0.03061224,-0.3061224,-0.3061176)"
        }
    )
    subgroup.create_path(
        "M 500,10 C 229.4,10 10,229.4 10,500 10,770.7 229.4,990 500,990 770.7,990 990,770.6 990,500 990,229.4 770.7,10 500,10 Z M 381.2,220.6 c 31.7,-31.7 73.8,-49.1 118.9,-49.1 44.9,0 87.3,17.4 118.7,49.1 32,31.8 49.5,73.9 49.5,118.9 0,44.9 -17.5,86.9 -49.5,118.7 -31.5,31.7 -73.8,49.3 -118.7,49.3 -45,0 -87.1,-17.5 -118.9,-49.3 -31.7,-31.7 -49.3,-73.9 -49.3,-118.7 0,-45 17.6,-87.1 49.3,-118.9 z M 500,895 C 374.1,895 260.3,843 179.2,759.2 216.1,653.8 314.8,573.9 424.7,573.9 h 150.5 c 109.7,0 208.6,79.9 245.6,185.2 C 739.6,843 625.9,895 500,895 Z"  # noqa: E501
    )


def add_posibility_for_star(svg):
    """
    add possibility for star
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'star',
                'view_box': '0 0 30 30'
            }
        )
    )
    subgroup = symbol.create_subgroup(
        "star_group",
        additional_arguments={
            "transform": "matrix(0.06765254,0,0,0.06765254,-2.4639587e-4,0.81711314)"
        }
    )
    subgroup.create_path(
        "m 436.083,190.376 -115.52,83.927 44.13,135.801 c 2.388,7.353 -0.236,15.403 -6.479,19.954 -3.139,2.271 -6.81,3.405 -10.498,3.405 -3.682,0 -7.364,-1.135 -10.479,-3.405 L 221.723,346.125 106.215,430.046 c -6.266,4.552 -14.733,4.552 -20.986,0 -6.239,-4.539 -8.866,-12.59 -6.475,-19.942 L 122.872,274.297 7.364,190.376 c -6.254,-4.545 -8.881,-12.593 -6.49,-19.948 2.397,-7.354 9.256,-12.33 16.979,-12.33 h 142.78 L 204.751,22.307 c 2.391,-7.353 9.245,-12.327 16.979,-12.327 7.734,0 14.576,4.974 16.964,12.327 l 44.118,135.791 h 142.792 c 7.72,0 14.576,4.977 16.976,12.33 2.37,7.355 -0.26,15.403 -6.497,19.948 z"  # noqa: E501
    )


def add_posibility_for_arrow(svg):
    """
    add possibility for arrow
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'arrow',
                'view_box': '0 0 30 30'
            }
        )
    )
    symbol.create_path(
        "m 20.201651,4.9909277 c -0.408701,-0.4229914 -1.088917,-0.4229914 -1.511908,0 -0.408701,0.4087012 -0.408701,1.0889171 0,1.4966656 l 7.666243,7.6662437 H 1.0584312 C 0.46872023,14.154789 0,14.62351 0,15.213221 c 0,0.589711 0.46872023,1.073674 1.0584312,1.073674 H 26.355986 l -7.666243,7.651953 c -0.408701,0.422991 -0.408701,1.10416 0,1.511908 0.422991,0.422992 1.10416,0.422992 1.511908,0 l 9.481105,-9.481105 c 0.422992,-0.408701 0.422992,-1.088917 0,-1.496665 z"  # noqa: E501
    )


def add_posibility_for_planet(svg):
    """
    add posibility for planet
    """
    symbol = Svg(
        etree.SubElement(
            svg.root,
            'symbol',
            {
                'id': 'planet',
                'view_box': '0 0 30 30'
            }
        )
    )
    symbol.create_path(
        "M 500,990 C 770.2,990 990,770.2 990,500 990,229.8 770.2,10 500,10 336.1,10 190.8,91 101.8,215 c -0.9,1.3 -1.9,2.6 -2.8,3.9 C 43,298.5 10,395.5 10,500 10,770.2 229.8,990 500,990 Z M 115.9,255.7 c 3.1,0.4 6.5,0.2 10.1,-0.9 214.5,-62.9 505.6,118.5 675.6,-88.6 1.2,-1.5 2.2,-3 3,-4.5 33.1,29.8 61.8,64.4 85,102.6 C 777.7,374.5 613.1,419 461,379.6 377.6,358 302.4,316.7 213.6,326.2 155,332.5 99.7,358.5 56.4,397.9 68.1,346.7 88.5,298.8 115.9,255.7 Z M 500,44.8 c 66.1,0 128.9,14.2 185.6,39.6 -87.6,23.6 -179.8,12 -259.1,-33.6 23.9,-3.9 48.5,-6 73.5,-6 z M 375.8,62.1 c -0.5,8 2.6,16.1 11.2,21.7 103,66.2 233.1,80.1 347.6,35.7 3.1,-1.2 5.7,-2.9 7.8,-4.8 8.5,5.4 16.9,11 25,17 -0.1,0.1 -0.1,0.1 -0.2,0.2 -72.7,88.5 -189.9,94.9 -295.8,84.3 C 367,205.6 263.7,180.7 160,197.4 216.8,133.6 291.3,86 375.8,62.1 Z M 935.5,367 c -138.7,58.1 -296.3,130.1 -448.7,107.7 -15,-2.9 -30,-6.1 -44.9,-9.6 -7.6,-2.1 -15.1,-4.4 -22.6,-7 -70.8,-24.9 -133.6,-61.1 -210.7,-61.2 -33.2,0 -65.7,6.9 -96.3,19 44.1,-30.9 97.1,-45.9 153.5,-42.3 86.2,5.6 164.1,56 250.5,65.7 144.4,16.1 290.8,-31.8 397.2,-130.3 8.4,18.8 15.9,38.1 22,58 z M 44.8,500 c 0,-0.6 0,-1.1 0,-1.7 0.8,-0.5 1.5,-1 2.3,-1.7 0.3,-0.3 0.6,-0.5 0.9,-0.7 -1.2,1.7 -2.1,3.5 -3.2,5.2 0,-0.3 0,-0.7 0,-1.1 z m 43.8,49.9 c -10.9,7.9 -21.2,16.5 -30.9,25.8 9.5,-10.2 19.8,-18.8 30.9,-25.8 z m -24.3,82.3 c 4.6,-1.2 8.3,-3.6 11,-6.8 2,-1.2 4,-2.6 5.9,-4.6 59.3,-62.4 140.5,-86.8 224.7,-71.6 80.5,14.6 154.4,47.8 236.7,55.6 146.8,13.9 295.8,-33.8 412.2,-122.6 0.2,5.9 0.4,11.8 0.4,17.7 0,36.7 -4.5,72.3 -12.7,106.5 -4.7,0.6 -9.4,2.9 -13.5,7.6 -32.3,36 -72.7,59.1 -117.8,68.1 -30.9,-19.1 -77.7,-13.6 -112.1,-10.5 -60.1,5.5 -112.6,13.9 -172.9,4.7 -52,-8 -103.4,-19.1 -155.5,-26.1 C 272.7,637 172.8,643 95.5,709 83,684.7 72.4,659 64.3,632.2 Z m 313.3,66.6 c 96.5,14.4 190.5,43.2 289,33.9 23.1,17.5 48.3,26.4 78.1,27.5 23.7,0.9 59,-8.2 74.1,-29.9 33.6,-6.4 65.4,-19.4 93.9,-38.2 -67.9,145.7 -210.6,249.3 -378.7,261.8 -0.8,-4.3 -3.1,-8.7 -7.3,-12.6 -88.6,-81.1 -205.6,-123 -325.6,-114.2 -5.1,0.4 -9.3,2.1 -12.8,4.5 -25.4,-23.9 -48.1,-50.7 -67.5,-79.8 69.3,-64.9 167.9,-66.2 256.8,-53 z",  # noqa: E501
        additional_arguments={
            "transform": "matrix(0.03061224,0,0,0.03061224,-0.3061224,-0.3061176)"
        }
    )


def add_posibility_for_symbol(svg, name):
    """
    add the symbol defined by name to svg
    """
    if name == "politician":
        add_posibility_for_politician(svg)
    elif name == "time":
        add_posibility_for_time(svg)
    elif name == "production":
        add_posibility_for_production(svg)
    elif name == "planet_rotation":
        add_posibility_for_planet_rotation(svg)
    elif name == "influence":
        add_posibility_for_influence(svg)
    elif name == "star":
        add_posibility_for_star(svg)
    elif name == "water":
        add_posibility_for_water(svg)
    elif name == "building_resource":
        add_posibility_for_building_res(svg)
    elif name == "coin":
        add_posibility_for_coin(svg)
    elif name == "disc_3d":
        add_posibility_for_disc_3d(svg)
    elif name == "resource_placeholder":
        add_posibility_for_empty_res(svg)
    elif name == "food":
        add_posibility_for_food(svg)
    elif name == "radioactive":
        add_posibility_for_radioactive(svg)
    elif name == "red_cross":
        add_posibility_for_red_cross(svg)
    elif name == "square_3d":
        add_posibility_for_square_3d(svg)
    elif name == "arrow":
        add_posibility_for_arrow(svg)
    elif name == "planet":
        add_posibility_for_planet(svg)


def main():
    """
    no main implemented
    """
    print("no main implemented")


if __name__ == '__main__':
    main()
