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


PLANETS = [
    Planet((150, 100), '#FF0000', 3, 'alpha'),
    Planet((210, 130), '#FF8000', 5, 'beta'),
    Planet((260, 180), '#FFFF00', 7, 'gamma'),
    Planet((320, 210), '#008000', 11, 'delta'),
    Planet((370, 240), '#1E90FF', 13, 'epsilon')
]

PLAYERS = [
    Player("player1", "#FF0000"),
    Player("player2", "#0000FF"),
    Player("player3", "#FFFFFF"),
    Player("player4", "#00FF00")
]

RESOURCE_BUY_PRICES = [2, 3, 4, 5, 6, 7]

RESOURCE_SELL_PRICES = [1, 2, 3, 4, 5, 6]
