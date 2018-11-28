#!/usr/bin/env python
"""
gamesettings
"""

class Planet(object):
    """
    Data class for one planet
    """
    def __init__(self, radius, col, number_hexes, planet_name):
        (radius_x, radius_y) = radius
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.colour = col
        self.number_of_hexes = number_hexes
        self.name = planet_name


class Player(object):
    """
    Data class for one player
    """
    def __init__(self, player_name, col):
        self.name = player_name
        self.colour = col

JSON_FILE = "gamesettings.json"
#with open(JSON_FILE, "r") as json_file:
#    JSON_CONTENT = json.load(json_file)

JSON_CONTENT = {
    "planets": [
        { 
            "name": "alpha",
            "radius": [150, 100],
            "colour": "#FF0000",
            "number_hexes": 3
        },
        {
            "name": "beta",
            "radius": [210, 130],
            "colour": "#FF8000",
            "number_hexes": 5
        },
        {
            "name": "gamma",
            "radius": [260, 180],
            "colour": "#FFFF00",
            "number_hexes": 7
        },
        {
            "name": "delta",
            "radius": [320, 210],
            "colour": "#008000",
            "number_hexes": 11
        },
        {
            "name": "epsilon",
            "radius": [370, 240],
            "colour": "#1E90FF",
            "number_hexes": 13
        }
    ],
    "players": [
        {
            "name": "player1",
            "colour": "#FF0000"
        },
        {
            "name": "player2",
            "colour": "#0000FF"
        },
        {
            "name": "player3",
            "colour": "#FFFFFF"
        },
        {
            "name": "player4",
            "colour": "#00FF00"
        }
    ],
    "resource_buy_prices": [2, 3, 4, 5, 6, 7],
    "resource_sell_prices": [1, 2, 3, 4, 5, 6]
}

PLANETS = [
    Planet(
        planet["radius"],
        planet["colour"],
        planet["number_hexes"],
        planet["name"]
    ) for planet in JSON_CONTENT["planets"]
]

PLAYERS = [
    Player(
        player["name"],
        player["colour"]
    ) for player in JSON_CONTENT["players"]
]

RESOURCE_BUY_PRICES = JSON_CONTENT["resource_buy_prices"]

RESOURCE_SELL_PRICES = JSON_CONTENT["resource_sell_prices"]
