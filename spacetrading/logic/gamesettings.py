"""
Consists of constants used throughout the game
"""

PLANET_ROTATION_TIME = 10
PLANET_ROTATION_MOVE = -5
OFFER_DEMAND_EVENT_TIMES = [40, 20, 15, 10]
OFFER_DEMAND_EVENT_MOVE = -6
FINISH_TIME = 80
MIDGAME_SCORING_TIME = FINISH_TIME/2
MIDGAME_SCORING_MOVE = -7
ADD_DEMAND_TIME = 17
ADD_DEMAND_MOVE = -8
FIRST_MOVE_NUMBER = 1

SETUP_PLANET_DEMAND_PRICE = [4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6]
SETUP_PLANET_SUPPLY_PRICE = [2, 2, 3, 3, 4, 4]
PLANET_DEMAND_MIN_PRICE = 2
PLANET_DEMAND_MAX_PRICE = 7
PLANET_SUPPLY_MIN_PRICE = 1
PLANET_SUPPLY_MAX_PRICE = 6

PLANETS = [
    [
        "alpha",
        3,
        "#FF0000",
        [[5, -2], [-3, 4], [-3, -1]],
        [150, 100],
        0
    ],
    [
        "beta",
        5,
        "#FF8000",
        [[7, -3], [1, 3], [-6, 5], [-5, 0], [3, -5]],
        [210, 130],
        0.2
    ],
    [
        "gamma",
        7,
        "#FFFF00",
        [[8, -2], [2, 4], [-5, 7], [-9, 5], [-6, -1], [2, -6], [7, -6]],
        [260, 180],
        0.4
    ],
    [
        "delta",
        11,
        "#008000",
        [[9, -1], [4, 4], [-2, 7], [-7, 8], [-10, 7], [-10, 3], [-7, -1],
         [-1, -6], [5, -8], [9, -8], [11, -5]],
        [320, 210],
        0.6
    ],
    [
        "epsilon",
        13,
        "#1E90FF",
        [[8, 1], [3, 5], [-2, 8], [-8, 9], [-11, 8], [-12, 5], [-11, 2],
         [-6, -3], [0, -7], [5, -9], [10, -9], [12, -7], [12, -4]],
        [370, 240],
        0.8
    ]
]

IDLE_MOVE_TIME = 4
