"""
Business logic how to handle a move
"""

from enum import Enum

from spacetrading.logic import gamesettings

class Event(Enum):
    """
    Enum of all Events
    """
    PLANET_ROTATION = 1
    OFFER_DEMAND = 2

def pass_game(game):
    """
    logic of the active player passing
    TODO: needs to be migrated with move
    """
    players = game.players.all()
    active_player = get_active_player(players)
    if active_player is None:
        finish_game(game)
        return

    active_player.has_passed = True
    active_player.save()

    players = game.players.all()
    active_player = get_active_player(players)
    if active_player is None:
        finish_game(game)
        return

def move(game, data):
    """
    logic of changing the game by data representing a move
    changes db or if move invalid throws an MoveError
    """
    players = game.players.all()
    active_player = get_active_player(players)
    planets = game.planets.all().order_by('number_of_hexes')
    active_planet_with_number = get_active_planet(active_player.ship_position, planets)
    active_planet = active_planet_with_number[0]
    planet_number = active_planet_with_number[1]
    trade_balance = get_trade_balance_or_raise(
        active_player, active_planet, planet_number, game, data
    )
    change_active_player(active_player, game.next_move_number, data, trade_balance)
    change_active_planet(active_planet, data)
    change_game(game, players, planets, planet_number, active_player.player_number, data)
    players = game.players.all()
    active_player = get_active_player(players)
    if active_player is None:
        finish_game(game)

class MoveError(Exception):
    """
    Exception class containing no additional information
    """

def get_trade_balance_or_raise(active_player, active_planet, planet_number, game, data):
    """
    returns value smaller than -active_player.money if move is not valid
    trading balance otherwise
    """
    if active_player is None:
        finish_game(game)
        raise MoveError("no active player")
    if active_player.ship_position == [data['coord_q'], data['coord_r']] or [data['coord_q'], data['coord_r']] == [0, 0]:
        raise MoveError("You need to fly to another place")

    buy_mapping = [
        ["buy_resource_1", '1'],
        ["buy_resource_2", '2'],
        ["buy_resource_3", '3'],
        ["buy_resource_4", '4'],
        ["buy_resource_5", '5']
    ]
    sell_mapping = [
        ["sell_resource_1", '1'],
        ["sell_resource_2", '2'],
        ["sell_resource_3", '3'],
        ["sell_resource_4", '4'],
        ["sell_resource_5", '5']
    ]

    trade_balance = 0
    traded = False

    number_of_resources = 0
    for resource in active_player.resources:
        number_of_resources = number_of_resources + resource

    for key, value in buy_mapping:
        if data[key] != 0:
            if active_planet is None:
                raise MoveError("You cannot trade, if you are not at a planet")
            if value not in active_planet.buy_resources:
                raise MoveError("You cannot trade the resources you selected at the planet you are")
            if data[key] + active_player.resources[int(value) - 1] > 9:
                raise MoveError("You cannot hold more than 9 resources")
            trade_balance = trade_balance - data[key]*active_planet.cost_buy_resource[active_planet.buy_resources.index(value)]
            number_of_resources = number_of_resources + data[key]
            traded = True

    for key, value in sell_mapping:
        if data[key] != 0:
            if active_planet is None:
                raise MoveError("You cannot trade, if you are not at a planet")
            if value not in active_planet.sell_resources:
                raise MoveError("You cannot trade the resources you selected at the planet you are")
            if data[key] > active_player.resources[int(value) - 1]:
                raise MoveError("You tried to sell more resources than you have")
            trade_balance = trade_balance + data[key]*active_planet.cost_sell_resource[active_planet.sell_resources.index(value)]
            number_of_resources = number_of_resources - data[key]
            traded = True
    if active_planet is None and data["buy_influence"] != 0:
        raise MoveError("You cannot trade, if you are not at a planet")
    if number_of_resources > 9:
        raise MoveError("You cannot hold more than 9 resources")

    trade_balance = trade_balance - get_cost_influence(traded, data["buy_influence"], game.planet_influence_track[planet_number][active_player.player_number])
    if trade_balance + active_player.money < 0:
        raise MoveError("You have not enough money")
    return trade_balance

def get_active_planet(ship_position, planets):
    """
    ship_position = [q, r]
    planets is a list of the planets in the game
    returns [planet, #indexOfPlanet] if at a planet
    returns [None, -1] otherwise
    """
    for index, planet in enumerate(planets):
        if ship_position == planet.position_of_hexes[planet.current_position]:
            return [planet, index]
    return [None, -1]

def get_cost_influence(did_we_trade, amount_influence, current_influence):
    """
    returns how much it costs to buy amount_influence if did_we_trade and have current_influence
    """
    if amount_influence == 0:
        return 0
    cost = 0
    if did_we_trade:
        cost = cost + 1
        amount_influence = amount_influence - 1
        current_influence = current_influence + 1

    return cost + (2*current_influence + amount_influence + 1)*amount_influence/2

def change_active_player(active_player, next_move_number, data, trade_balance):
    """
    performs changes on active_player
    """
    if active_player.last_move < 0:
        active_player.time_spent = 0
    else:
        active_player.time_spent = active_player.time_spent + compute_distance(active_player.ship_position, [data['coord_q'], data['coord_r']])
    active_player.last_move = next_move_number
    active_player.ship_position = [data['coord_q'], data['coord_r']]
    active_player.money = active_player.money + trade_balance
    active_player.resources[0] = active_player.resources[0] + data["buy_resource_1"] - data["sell_resource_1"]
    active_player.resources[1] = active_player.resources[1] + data["buy_resource_2"] - data["sell_resource_2"]
    active_player.resources[2] = active_player.resources[2] + data["buy_resource_3"] - data["sell_resource_3"]
    active_player.resources[3] = active_player.resources[3] + data["buy_resource_4"] - data["sell_resource_4"]
    active_player.resources[4] = active_player.resources[4] + data["buy_resource_5"] - data["sell_resource_5"]
    active_player.save()

def change_active_planet(active_planet, data):
    """
    performs changes on active_planet
    """
    if active_planet is None:
        return
    for resource in active_planet.buy_resources:
        key = "buy_resource_{}".format(resource)
        if resource != '0' and data[key] != 0:
            index = active_planet.buy_resources.index(resource)
            active_planet.cost_buy_resource[index] = min(active_planet.cost_buy_resource[index] + 1, 8)
    for resource in active_planet.sell_resources:
        key = "sell_resource_{}".format(resource)
        if resource != '0' and data[key] != 0:
            index = active_planet.sell_resources.index(resource)
            active_planet.cost_sell_resource[index] = max(active_planet.cost_sell_resource[index] - 1, 2)
    active_planet.save()


def change_game(game, players, planets, active_planet_number, active_player_number, data):
    """
    performs changes on game
    """
    game.next_move_number = game.next_move_number + 1
    next_event = get_next_event(game, players)
    while next_event is not None:
        if next_event == Event.PLANET_ROTATION:
            planet_rotation(game, players, planets)
        elif next_event == Event.OFFER_DEMAND:
            offer_demand(game, planets)
        next_event = get_next_event(game, players)
    game.planet_influence_track[active_planet_number][active_player_number] = game.planet_influence_track[active_planet_number][active_player_number] + data["buy_influence"]
    game.save()

def finish_game(game):
    """
    sets the game status to finished
    """
    game.game_state = 'f'
    game.save()

def compute_distance(coordinates1, coordinates2):
    """
    computes how long the ships needs to fly from coordinates1 to coordinates2
    """
    absolute_distance = max(
        abs(coordinates1[0]-coordinates2[0]),
        abs(coordinates1[1]-coordinates2[1]),
        abs(coordinates1[0]+coordinates1[1]-coordinates2[0]-coordinates2[1])
    )
    return absolute_distance + 2

def get_next_event(game, players):
    """
    return None if a player has to move before the next event
    otherwise return the corresponding Event enum entry
    """
    planet_rotation_event = [game.planet_rotation_event_time, game.planet_rotation_event_move]
    offer_demand_event = [game.offer_demand_event_time, game.offer_demand_event_move]
    active_player = get_active_player(players)
    if active_player is None:
        return None
    if is_before(planet_rotation_event, offer_demand_event):
        if is_before(planet_rotation_event, [active_player.time_spent, active_player.last_move]):
            return Event.PLANET_ROTATION
    else:
        if is_before(offer_demand_event, [active_player.time_spent, active_player.last_move]):
            return Event.OFFER_DEMAND

    return None

def planet_rotation(game, players, planets):
    """
    move planets and player positions which are located at planets
    increase event time
    set event move
    increase turn counter
    """
    game.planet_rotation_event_time = game.planet_rotation_event_time + gamesettings.PLANET_ROTATION_TIME
    game.planet_rotation_event_move = game.next_move_number
    game.next_move_number = game.next_move_number + 1
    game.save()
    for planet in planets:
        current_hex_position = planet.position_of_hexes[planet.current_position]
        planet.current_position = (planet.current_position + 1) % planet.number_of_hexes
        next_hex_position = planet.position_of_hexes[planet.current_position]
        planet.save()
        for player in players:
            if player.ship_position == current_hex_position:
                player.ship_position = next_hex_position
                player.save()

def offer_demand(game, planets):
    """
    adjust offer_demand prices
    increase event time
    set event move
    increase turn counter
    """
    game.offer_demand_event_time = game.offer_demand_event_time + gamesettings.OFFER_DEMAND_EVENT_TIMES[game.number_of_players - 1]
    game.offer_demand_event_move = game.next_move_number
    game.next_move_number = game.next_move_number + 1
    game.save()
    for planet in planets:
        for index, price in enumerate(planet.cost_buy_resource):
            planet.cost_buy_resource[index] = max(1, price - 1)
        for index, price in enumerate(planet.cost_sell_resource):
            planet.cost_sell_resource[index] = min(7, price + 1)
        planet.save()

def get_active_player(players):
    """
    returns the active_player or None (not considering events)
    """
    active_player = None
    for player in players:
        if player.has_passed or player.time_spent > 100:
            continue
        if active_player is None:
            active_player = player
            continue
        if player_is_before(player, active_player):
            active_player = player
    return active_player

def player_is_before(player1, player2):
    """
    returns True if player1 moves before player2
    """
    if player1.has_passed:
        return False
    if player2.has_passed:
        return True
    return is_before([player1.time_spent, player1.last_move], [player2.time_spent, player2.last_move])

def is_before(one, two):
    """
    return True if ones turn is before twos,
    where one, two = [time_spent, last_move_number]
    """
    if one[0] < two[0] or (one[0] == two[0] and one[1] > two[1]):
        return True
    return False

def compute_points(game, player_number):
    """
    compute the points in game of the player with player_number
    """
    result = 0
    planet_points = [5, 3, 2, 1]
    for planet_influence in game.planet_influence_track:
        current_player_influence = planet_influence[player_number]
        if current_player_influence == 0:
            continue
        rated_higher = sum(i > current_player_influence for i in planet_influence)
        rated_same = sum(i == current_player_influence for i in planet_influence)
        result = result + int(sum(planet_points[rated_higher : rated_higher + rated_same])/rated_same)

    return result
