#!/usr/bin/env python
"""
generate the main gameboard
"""
from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg import generate_svg_symbols

WIDTH = 120
HEIGHT = 180

class Action:
    def __init__(self, times_, left_, right_):
        self.times = times_
        self.left = left_
        self.right = right_

def get_relative_location(number_of_symbols):
    if number_of_symbols == 1:
        return [[20, 20]]
    elif number_of_symbols == 2:
        return [[10, 20], [30, 20]]
    elif number_of_symbols == 3:
        return [[10, 10], [30, 10], [20, 30]]
    elif number_of_symbols == 4:
        return [[10, 10], [30, 10], [10, 30], [30, 30]]
    return []

def get_symbol_size(name):
    if name == "politician":
        return 30
    elif name == "time":
        return 20
    elif name == "production":
        return 30
    elif name == "planet_rotation":
        return 30
    elif name == "influence":
        return 20
    elif name == "star":
        return 30
    elif name == "water":
        return 20
    elif name == "building_resource":
        return 20
    elif name == "coin":
        return 20
    elif name == "resource_placeholder":
        return 20
    elif name == "food":
        return 20
    elif name == "radioactive":
        return 20
    elif name == "red_cross":
        return 20
    print(name)
    return 0

def draw_politician(name, colour, points, era, actions):
    svg = Svg(width=str(WIDTH + 4), height=str(HEIGHT + 4), id_name=f"id_{name}")
    generate_svg_symbols.add_posibility_for_politician(svg)
    generate_svg_symbols.add_posibility_for_arrow(svg)
    generate_svg_symbols.add_posibility_for_influence(svg)
    generate_svg_symbols.add_posibility_for_time(svg)
    generate_svg_symbols.add_posibility_for_building_res(svg)
    generate_svg_symbols.add_posibility_for_coin(svg)
    generate_svg_symbols.add_posibility_for_food(svg)
    generate_svg_symbols.add_posibility_for_radioactive(svg)
    generate_svg_symbols.add_posibility_for_red_cross(svg)
    generate_svg_symbols.add_posibility_for_water(svg)
    svg.create_rectangle(
        [2, 2],
        [WIDTH, HEIGHT],
        f"border_{name}",
        fill_colour=colour,
        stroke_colour="black",
        stroke_width="2",
        additional_arguments={
            "rx" : "20",
            "ry" : "20"
        }
    )

    size_x = 100
    size_y = 40
    size_arrow = 15
    gap_x = (WIDTH - size_x)/2
    gap_y = (HEIGHT - 3*size_y)/12
    for i in range(3):
        svg.create_rectangle(
            [2 + gap_x, 2 + (i+5)*gap_y + i*size_y],
            [size_x, size_y],
            f"action_{i}_{name}",
            fill_colour="white",
            stroke_colour="black",
            additional_arguments={
                "rx": "10",
                "ry": "10"
            }
        )
        
        scale_arrow = size_arrow/30
        svg.use_symbol(
            "arrow",
            f"arrow_{i}_{name}",
            position=[
                (2 + gap_x + (size_x-size_arrow)/2)/scale_arrow,
                (2 + (i+5)*gap_y + (i+0.5)*size_y - size_arrow/2)/scale_arrow
            ],
            additional_arguments={
                "transform": f"scale({scale_arrow})"
            }
        )
        svg.create_text(
            f"text_{i}_name_above_arrow",
            [
                2 + gap_x + size_x/2 - 3,
                2 + (i+5)*gap_y + (i+0.5)*size_y - 3
            ],
            f"{actions[i].times}x",
            font_size="6"
        )

    gap_politician = 2
    size_politician = 15
    scale_factor = size_politician/30
    offset_x = gap_x
    start_y = 2 + 8*gap_y + 3*size_y
    if len(points) == 1:
        winner_points = points[0]
        start_x = 2 + WIDTH - offset_x - winner_points*size_politician - (winner_points - 1)*gap_politician
        for i in range(winner_points):
            svg.use_symbol(
                "politician",
                f"politician_points_{i}_{name}",
                position=[(start_x + i*(size_politician+gap_politician))/scale_factor, start_y/scale_factor],
                additional_arguments={
                    "transform": f"scale({scale_factor})"
                }
            )
    else:
        font_size = 10
        start_x = 2 + gap_x + 4
        for i, player_points in enumerate(points):
            svg.create_text(
                f"politician_points_{i}_{name}",
                [start_x + i*25, start_y + (size_politician + font_size)/2],
                str(player_points),
                font_size=font_size
            )
            svg.use_symbol(
                "politician",
                f"politician_points_symbol_{i}_{name}",
                position=[(start_x + 4 + i*25)/scale_factor, start_y/scale_factor],
                additional_arguments={
                    "transform": f"scale({scale_factor})"
                }
            )
    for action_number, action in enumerate(actions):
        
        top = 2 + (action_number+5)*gap_y + action_number*size_y
        left = 2 + gap_x
        symbol_size = 12
        positions_symbols = get_relative_location(len(action.left))
        for index, symbol_name in enumerate(action.left):
            position = positions_symbols[index]
            position[0] = position[0] + left - symbol_size/2
            position[1] = position[1] + top - symbol_size/2
            symbol_original_size = get_symbol_size(symbol_name[1])
            scale_factor = symbol_size/symbol_original_size
            font_size = 6
            svg.create_text(
                f"left_text_{symbol_name[1]}_{index}_{action_number}_{name}",
                [position[0]+1, position[1] + (symbol_size + font_size)/2],
                str(symbol_name[0]),
                font_size=font_size
            )

            svg.use_symbol(
                symbol_name[1],
                f"left_symbol_{symbol_name[1]}_{index}_{action_number}_{name}",
                position=[(position[0] + 5)/scale_factor, position[1]/scale_factor],
                additional_arguments={
                    "transform": f"scale({scale_factor})"
                }
            )
        left = 2 + gap_x + size_x/2 + 10
        positions_symbols = get_relative_location(len(action.right))
        for index, symbol_name in enumerate(action.right):
            position = positions_symbols[index]
            position[0] = position[0] + left - symbol_size/2
            position[1] = position[1] + top - symbol_size/2
            symbol_original_size = get_symbol_size(symbol_name[1])
            scale_factor = symbol_size/symbol_original_size
            font_size = 6
            svg.create_text(
                f"right_text_{symbol_name[1]}_{index}_{action_number}_{name}",
                [position[0]+3, position[1] + (symbol_size + font_size)/2],
                str(symbol_name[0]),
                font_size=font_size,
                text_anchor='end'
            )

            svg.use_symbol(
                symbol_name[1],
                f"right_symbol_{symbol_name[1]}_{index}_{action_number}_{name}",
                position=[(position[0] + 3)/scale_factor, position[1]/scale_factor],
                additional_arguments={
                    "transform": f"scale({scale_factor})"
                }
            )

    return svg
    
def draw_politicians(planets):
    """
    draw all politicians
    """
    svgs = []
    cards = [
        [
            [
                [
                    Action(3, [[1, 'time']], [[2, 'influence']]),
                    Action(3, [[4, 'coin'], [1, 'time']], [[1, 'building_resource'], [1, 'influence']]),
                    Action(2, [[1, 'water'], [1, 'time']], [[6, 'coin']])
                ],
                1,
                [1]
            ],
            [
                [
                    Action(3, [[2, 'time']], [[1, 'influence']]),
                    Action(3, [[3, 'coin'], [1, 'time']], [[1, 'building_resource']]),
                    Action(3, [[1, 'water'], [2, 'time']], [[7, 'coin']])
                ],
                1,
                [1]
            ],
            [
                [
                    Action(3, [[2, 'time'], [2, 'coin']], [[1, 'influence']]),
                    Action(3, [[4, 'coin'], [1, 'time']], [[1, 'building_resource']]),
                    Action(2, [[1, 'food'], [1, 'water'], [3, 'time']], [[16, 'coin'], [1, 'influence']])
                ],
                2,
                [3]
            ],
            [
                [
                    Action(1, [[1, 'water']], [[5, 'influence']]),
                    Action(3, [[1, 'water'], [1, 'time']], [[1, 'building_resource'], [1, 'influence'], [2, 'coin']]),
                    Action(2, [[1, 'water'], [1, 'red_cross'], [2, 'time']], [[15, 'coin'], [2, 'influence']])
                ],
                2,
                [3]
            ],
            [
                [
                    Action(3, [[1, 'water'], [1, 'red_cross'], [2, 'time']], [[1, 'building_resource'], [1, 'influence']]),
                    Action(3, [[1, 'water'], [1, 'food'], [2, 'time']], [[6, 'coin'], [1, 'influence']]),
                    Action(1, [[1, 'water'], [1, 'food'], [1, 'red_cross'], [2, 'time']], [[5, 'influence']])
                ],
                3,
                [7, 4, 2, 1]
            ],
            [
                [
                    Action(3, [[3, 'time']], [[1, 'influence']]),
                    Action(3, [[1, 'politician'], [1, 'time']], [[7, 'influence']]),
                    Action(1, [[1, 'water'], [1, 'food'], [1, 'red_cross'], [4, 'coin']], [[10, 'influence']])
                ],
                3,
                [7, 4, 2, 1]
            ]
        ],
        ################################
        [
            [
                [
                    Action(3, [[1, 'time']], [[2, 'influence']]),
                    Action(3, [[3, 'coin'], [1, 'time']], [[1, 'food'], [1, 'influence']]),
                    Action(2, [[1, 'red_cross']], [[5, 'coin']])
                ],
                1,
                [1]
            ],
            [
                [
                    Action(3, [[2, 'time']], [[1, 'influence']]),
                    Action(3, [[3, 'coin'], [1, 'time']], [[1, 'food']]),
                    Action(3, [[1, 'red_cross'], [2, 'time']], [[6, 'coin']])
                ],
                1,
                [1]
            ],
            [
                [
                    Action(3, [[5, 'coin']], [[1, 'influence']]),
                    Action(3, [[4, 'coin'], [1, 'time']], [[1, 'food']]),
                    Action(2, [[1, 'red_cross'], [1, 'radioactive'], [3, 'time']], [[16, 'coin'], [1, 'influence']])
                ],
                2,
                [3]
            ],
            [
                [
                    Action(1, [[1, 'red_cross']], [[2, 'influence'], [3, 'coin']]),
                    Action(3, [[1, 'red_cross'], [2, 'time']], [[1, 'food'], [1, 'influence'], [3, 'coin']]),
                    Action(2, [[1, 'red_cross'], [1, 'water'], [3, 'time']], [[15, 'coin'], [3, 'influence']])
                ],
                2,
                [3]
            ],
            [
                [
                    Action(3, [[1, 'red_cross'], [1, 'radioactive'], [5, 'time']], [[1, 'food'], [2, 'influence']]),
                    Action(3, [[1, 'red_cross'], [1, 'water'], [2, 'time']], [[6, 'coin'], [1, 'influence']]),
                    Action(1, [[1, 'red_cross'], [1, 'radioactive'], [1, 'water'], [1, 'time']], [[5, 'influence']])
                ],
                3,
                [7, 4, 2, 1]
            ],
            [
                [
                    Action(3, [[3, 'time'], [4, 'coin']], [[1, 'influence']]),
                    Action(3, [[1, 'politician'], [1, 'time']], [[2, 'influence']]),
                    Action(1, [[1, 'red_cross'], [1, 'radioactive'], [1, 'water']], [[2, 'influence']])
                ],
                3,
                [7, 4, 2, 1]
            ]
        ],
        ################################
        [
            [
                [
                    Action(3, [[2, 'time']], [[3, 'influence']]),
                    Action(3, [[4, 'coin'], [1, 'time']], [[1, 'radioactive'], [1, 'influence']]),
                    Action(2, [[1, 'food'], [3, 'time']], [[6, 'coin'], [1, 'influence']])
                ],
                1,
                [1]
            ],
            [
                [
                    Action(3, [[2, 'time']], [[1, 'influence']]),
                    Action(3, [[3, 'coin'], [1, 'time']], [[1, 'radioactive']]),
                    Action(3, [[1, 'food'], [2, 'time']], [[7, 'coin']])
                ],
                1,
                [1]
            ],
            [
                [
                    Action(3, [[2, 'time'], [2, 'coin']], [[1, 'influence']]),
                    Action(3, [[4, 'coin'], [2, 'time']], [[1, 'radioactive'], [1, 'influence']]),
                    Action(2, [[1, 'food'], [1, 'water'], [3, 'time']], [[16, 'coin'], [1, 'influence']])
                ],
                2,
                [3]
            ],
            [
                [
                    Action(1, [[2, 'food']], [[5, 'influence'], [6, 'coin']]),
                    Action(3, [[1, 'food'], [1, 'time']], [[1, 'radioactive'], [1, 'influence'], [2, 'coin']]),
                    Action(2, [[1, 'food'], [1, 'building_resource'], [2, 'time']], [[15, 'coin'], [2, 'influence']])
                ],
                2,
                [3]
            ],
            [
                [
                    Action(3, [[1, 'food'], [1, 'building_resource'], [2, 'time']], [[1, 'radioactive'], [1, 'influence']]),
                    Action(3, [[1, 'food'], [1, 'water'], [2, 'time']], [[6, 'coin'], [1, 'influence']]),
                    Action(1, [[1, 'food'], [1, 'water'], [1, 'building_resource'], [2, 'time']], [[5, 'influence']])
                ],
                3,
                [7, 4, 2, 1]
            ],
            [
                [
                    Action(3, [[3, 'time']], [[1, 'influence']]),
                    Action(3, [[1, 'politician'], [1, 'time']], [[7, 'influence']]),
                    Action(1, [[1, 'food'], [1, 'water'], [10, 'coin']], [[10, 'influence']])
                ],
                3,
                [7, 4, 2, 1]
            ]
        ],
        ################################
        [
            [
                [
                    Action(3, [[2, 'time']], [[3, 'influence']]),
                    Action(3, [[4, 'coin'], [1, 'time']], [[1, 'red_cross'], [1, 'influence']]),
                    Action(2, [[1, 'building_resource'], [1, 'time']], [[6, 'coin']])
                ],
                1,
                [1]
            ],
            [
                [
                    Action(3, [[2, 'time']], [[1, 'influence']]),
                    Action(3, [[4, 'coin']], [[1, 'red_cross']]),
                    Action(3, [[1, 'building_resource'], [2, 'time']], [[7, 'coin']])
                ],
                1,
                [1]
            ],
            [
                [
                    Action(3, [[2, 'time'], [5, 'coin']], [[2, 'influence']]),
                    Action(3, [[4, 'coin'], [1, 'time']], [[1, 'red_cross']]),
                    Action(2, [[1, 'building_resource'], [1, 'radioactive'], [1, 'time']], [[15, 'coin'], [1, 'influence']])
                ],
                2,
                [3]
            ],
            [
                [
                    Action(1, [[1, 'building_resource']], [[5, 'influence']]),
                    Action(3, [[1, 'building_resource'], [1, 'time']], [[1, 'red_cross'], [1, 'influence'], [2, 'coin']]),
                    Action(2, [[1, 'building_resource'], [1, 'food'], [2, 'time']], [[15, 'coin'], [2, 'influence']])
                ],
                2,
                [3]
            ],
            [
                [
                    Action(3, [[1, 'building_resource'], [1, 'radioactive'], [2, 'time']], [[1, 'red_cross'], [1, 'influence']]),
                    Action(3, [[1, 'building_resource'], [1, 'food'], [2, 'time']], [[6, 'coin'], [1, 'influence']]),
                    Action(1, [[1, 'building_resource'], [1, 'food'], [1, 'radioactive'], [4, 'coin']], [[5, 'influence']])
                ],
                3,
                [7, 4, 2, 1]
            ],
            [
                [
                    Action(3, [[3, 'time']], [[1, 'influence']]),
                    Action(3, [[10, 'coin']], [[3, 'influence']]),
                    Action(1, [[1, 'building_resource'], [1, 'food'], [1, 'radioactive']], [[8, 'influence']])
                ],
                3,
                [7, 4, 2, 1]
            ]
        ],
        ################################
        [
            [
                [
                    Action(3, [[1, 'time']], [[2, 'influence']]),
                    Action(3, [[4, 'coin'], [1, 'time']], [[1, 'water'], [1, 'influence']]),
                    Action(2, [[1, 'radioactive'], [1, 'time']], [[5, 'coin'], [1, 'influence']])
                ],
                1,
                [1]
            ],
            [
                [
                    Action(3, [[2, 'time']], [[1, 'influence']]),
                    Action(2, [[2, 'coin'], [2, 'time']], [[1, 'water']]),
                    Action(3, [[1, 'radioactive'], [2, 'time']], [[7, 'coin']])
                ],
                1,
                [1]
            ],
            [
                [
                    Action(3, [[2, 'time'], [2, 'coin']], [[1, 'influence']]),
                    Action(3, [[4, 'coin'], [1, 'time']], [[1, 'water']]),
                    Action(2, [[1, 'radioactive'], [1, 'building_resource'], [3, 'time']], [[16, 'coin'], [1, 'influence']])
                ],
                2,
                [3]
            ],
            [
                [
                    Action(2, [[1, 'radioactive']], [[3, 'influence'], [3, 'coin']]),
                    Action(3, [[1, 'radioactive'], [1, 'time']], [[1, 'water'], [1, 'influence'], [2, 'coin']]),
                    Action(2, [[1, 'radioactive'], [1, 'red_cross'], [2, 'time']], [[15, 'coin'], [2, 'influence']])
                ],
                2,
                [3]
            ],
            [
                [
                    Action(3, [[1, 'radioactive'], [1, 'red_cross'], [2, 'time']], [[1, 'water'], [1, 'influence']]),
                    Action(3, [[1, 'radioactive'], [1, 'building_resource'], [2, 'time']], [[6, 'coin'], [1, 'influence']]),
                    Action(1, [[1, 'radioactive'], [1, 'building_resource'], [1, 'red_cross'], [5, 'coin']], [[5, 'influence']])
                ],
                3,
                [7, 4, 2, 1]
            ],
            [
                [
                    Action(3, [[1, 'time'], [4, 'coin']], [[1, 'influence']]),
                    Action(3, [[1, 'politician'], [1, 'time']], [[7, 'influence']]),
                    Action(1, [[1, 'radioactive'], [1, 'building_resource'], [1, 'red_cross'], [4, 'coin']], [[10, 'influence']])
                ],
                3,
                [7, 4, 2, 1]
            ]
        ]
    ]
    for index, planet in enumerate(planets):
        for card in cards[index]:
            svgs.append(
                draw_politician(
                    planet.name,
                    planet.colour,
                    card[2],
                    card[1],
                    card[0]
                )
            )
    return svgs

if __name__ == '__main__':
    pass
