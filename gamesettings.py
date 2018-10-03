#!/usr/bin/env python
"""
gamesettings
"""
import json

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
with open(JSON_FILE, "r") as json_file:
    JSON_CONTENT = json.load(json_file)

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
