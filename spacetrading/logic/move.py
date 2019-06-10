"""
Business logic how to handle a move
"""

from enum import Enum

from spacetrading.logic import gamesettings


PLANET_DEMAND_MAPPING = {str(i) : "planet_demand_resource_{}".format(i) for i in range(1, 6)}
PLANET_SUPPLY_MAPPING = {str(i) : "planet_supply_resource_{}".format(i) for i in range(1, 6)}


class Event(Enum):
    """
    Enum of all Events
    """
    PLANET_ROTATION = 1
    OFFER_DEMAND = 2
    MIDGAME_SCORING = 3


def move(game, data):
    """
    logic of changing the game by data representing a move
    changes db or if move invalid throws an MoveError
    """
    players = game.players.all()
    active_player = get_active_player(players)
    planets = game.planets.all().order_by('planet_number')
    active_planet = get_active_planet(
        active_player.ship_position, planets)
    trade_balance = get_trade_balance_or_raise(
        active_player, active_planet, game, data
    )
    change_active_player(
        active_player, active_planet, game.next_move_number, data, trade_balance
    )
    change_active_planet(active_planet, data)
    change_game(game, players, planets, active_planet,
                active_player.player_number, data)
    players = game.players.all()
    active_player = get_active_player(players)
    if active_player is None:
        finish_game(game)


class MoveError(Exception):
    """
    Exception class containing no additional information
    """


def get_trade_balance_or_raise(active_player, active_planet, game, data):
    """
    returns value smaller than -active_player.money if move is not valid
    trading balance otherwise
    """
    if active_player is None:
        finish_game(game)
        raise MoveError("no active player")
    if data.get('move_type', 'Regular') is 'Regular':
        if data.get('coord_q', None) is None or \
            data.get('coord_r', None) is None or \
            [data['coord_q'], data['coord_r']] == [0, 0]:
            raise MoveError("You didn't choose where to fly.")
        distance = compute_distance(
            active_player.ship_position,
            [data['coord_q'], data['coord_r']]
        )
        if active_player.last_move >= 0:
            if data.get('spend_time') is not None and distance > data.get('spend_time', 0):
                raise MoveError(
                    "You want to spend {} time, but the distance to you destination is {}".format(
                        data.get('spend_time', 0), distance)
                )
            if data.get('spend_time') is None:
                raise MoveError("You need to specify a time you want to spend.")

    trade_balance = 0
    traded = False

    if active_planet is None:
        return trade_balance

    for resource in active_planet.planet_demand_resources:
        if resource != '0':
            if data.get(PLANET_DEMAND_MAPPING[resource], 0) + active_player.resources[int(resource) - 1] > game.resource_limit:
                raise MoveError(
                    "You cannot hold more than {} of one resource".format(game.resource_limit))
            if data.get(PLANET_DEMAND_MAPPING[resource], 0) > 0:
                trade_balance = trade_balance - \
                    data[PLANET_DEMAND_MAPPING[resource]] * \
                        active_planet.planet_demand_resources_price[active_planet.planet_demand_resources.index(resource)]
                traded = True

    for resource in active_planet.planet_supply_resources:
        if resource != '0':
            if data.get(PLANET_SUPPLY_MAPPING[resource], 0) > active_player.resources[int(resource) - 1]:
                raise MoveError(
                    "You tried to sell more resources than you have")
            if data.get(PLANET_SUPPLY_MAPPING[resource], 0) > 0:
                trade_balance = trade_balance + \
                    data[PLANET_SUPPLY_MAPPING[resource]] * \
                        active_planet.planet_supply_resources_price[active_planet.planet_supply_resources.index(resource)]
                traded = True

    trade_balance = trade_balance - get_cost_influence(
        traded, data.get("buy_influence", 0), game.planet_influence_track[active_planet.planet_number][active_player.player_number])
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
    for planet in planets:
        if ship_position == planet.position_of_hexes[planet.current_position]:
            return planet
    return None


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


def change_active_player(active_player, active_planet, next_move_number, data, trade_balance):
    """
    performs changes on active_player
    """
    if data.get('move_type', 'Regular') is 'Regular':
        if active_player.last_move < 0:
            active_player.time_spent = 0
        else:
            active_player.time_spent = active_player.time_spent + \
                data['spend_time']
        active_player.last_move = next_move_number
        active_player.ship_position = [data['coord_q'], data['coord_r']]
    elif data.get('move_type', 'Regular') is 'Pass':
        active_player.has_passed = True

    if active_planet is not None:
        active_player.money = active_player.money + trade_balance
        for resource in active_planet.planet_demand_resources:
            if resource != "0":
                active_player.resources[int(resource) - 1] += data.get(PLANET_DEMAND_MAPPING[resource], 0)
        for resource in active_planet.planet_supply_resources:
            if resource != "0":
                active_player.resources[int(resource) - 1] -= data.get(PLANET_SUPPLY_MAPPING[resource], 0)

    active_player.save()


def change_active_planet(active_planet, data):
    """
    performs changes on active_planet
    """
    if active_planet is None:
        return
    for resource in active_planet.planet_demand_resources:
        if resource != '0' and data[PLANET_DEMAND_MAPPING[resource]] != 0:
            index = active_planet.planet_demand_resources.index(resource)
            active_planet.planet_demand_resources_price[index] = min(
                active_planet.planet_demand_resources_price[index] + 1, gamesettings.PLANET_DEMAND_MAX_PRICE)
    for resource in active_planet.planet_supply_resources:
        if resource != '0' and data[PLANET_SUPPLY_MAPPING[resource]] != 0:
            index = active_planet.planet_supply_resources.index(resource)
            active_planet.planet_supply_resources_price[index] = max(
                active_planet.planet_supply_resources_price[index] - 1, gamesettings.PLANET_SUPPLY_MIN_PRICE)
    active_planet.save()


def change_game(game, players, planets, active_planet, active_player_number, data):
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
        elif next_event == Event.MIDGAME_SCORING:
            midgame_scoring(game, players)
        next_event = get_next_event(game, players)
    if active_planet is not None:
        active_planet_number = active_planet.planet_number
        game.planet_influence_track[active_planet_number][active_player_number] = game.planet_influence_track[
            active_planet_number][active_player_number] + data.get("buy_influence", 0)
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
    if coordinates1 == coordinates2:
        return gamesettings.IDLE_MOVE_TIME

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
    active_player = get_active_player(players)
    if active_player is None:
        return None

    planet_rotation_event = (
        game.planet_rotation_event_time, game.planet_rotation_event_move, Event.PLANET_ROTATION)
    offer_demand_event = (game.offer_demand_event_time,
                          game.offer_demand_event_move, Event.OFFER_DEMAND)
    no_event = (active_player.time_spent, active_player.last_move, None)
    events = [planet_rotation_event, offer_demand_event, no_event]

    if game.midgame_scoring:
        midgame_scoring_event = (game.midgame_scoring_event_time, game.midgame_scoring_event_move, Event.MIDGAME_SCORING)
        events.append(midgame_scoring_event)
    result = next_turn(events)

    return result

def next_turn(events):
    """
    list of (turn, move, returnvalue)
    return returnvalue where turn is smallest, on tie move is largest
    """
    return sorted(events, key=lambda tup: (tup[0], -tup[1]))[0][2]


def planet_rotation(game, players, planets):
    """
    move planets and player positions which are located at planets
    increase event time
    set event move
    increase turn counter
    """
    game.planet_rotation_event_time = game.planet_rotation_event_time + \
        gamesettings.PLANET_ROTATION_TIME
    game.planet_rotation_event_move = game.next_move_number
    game.next_move_number = game.next_move_number + 1
    game.save()
    for planet in planets:
        current_hex_position = planet.position_of_hexes[planet.current_position]
        planet.current_position = (
            planet.current_position + 1) % planet.number_of_hexes
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
    game.offer_demand_event_time = game.offer_demand_event_time + \
        gamesettings.OFFER_DEMAND_EVENT_TIMES[game.number_of_players - 1]
    game.offer_demand_event_move = game.next_move_number
    game.next_move_number = game.next_move_number + 1
    game.save()
    for planet in planets:
        for index, price in enumerate(planet.planet_demand_resources_price):
            planet.planet_demand_resources_price[index] = max(gamesettings.PLANET_DEMAND_MIN_PRICE, price - 1)
        for index, price in enumerate(planet.planet_supply_resources_price):
            planet.planet_supply_resources_price[index] = min(gamesettings.PLANET_SUPPLY_MAX_PRICE, price + 1)
        planet.save()


def midgame_scoring(game, players):
    """
    score 2 points for 1st player in a planet,
    1 point for 2nd
    both only if scored at all
    """
    game.midgame_scoring_event_time = 100
    game.midgame_scoring_event_move = game.next_move_number
    game.next_move_number = game.next_move_number + 1
    game.save()
    for player in players:
        points = compute_points(game, player, [2, 1])
        player.points = points
        player.save()


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


def compute_points(game, player, planet_points=None):
    """
    compute the points in game of the player with player_number
    """
    result = 0
    if planet_points is None:
        planet_points = [5, 3, 2, 1]
    for planet_influence in game.planet_influence_track:
        current_player_influence = planet_influence[player.player_number]
        if current_player_influence == 0:
            continue
        rated_higher = sum(
            i > current_player_influence for i in planet_influence)
        rated_same = sum(
            i == current_player_influence for i in planet_influence)
        result = result + \
            int(sum(
                planet_points[rated_higher: rated_higher + rated_same])/rated_same)

    return result + player.points
