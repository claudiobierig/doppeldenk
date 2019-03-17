from enum import Enum

from spacetrading import models

class EVENT_TYPE(Enum):
    PLANET_ROTATION = 1
    OFFER_DEMAND = 2

def move(game, data):
    players = game.players.all()
    planets = game.planets.all()
    active_player = get_active_player(players)
    if active_player.last_move < 0:
        active_player.time_spent = 0
    else:
        active_player.time_spent = active_player.time_spent + compute_distance(active_player.ship_position, [data['coord_q'], data['coord_r']])
    
    active_player.last_move = game.next_move_number
    game.next_move_number = game.next_move_number + 1
    active_player.ship_position = [data['coord_q'], data['coord_r']]
    next_event = get_next_event(game, players)
    while next_event is not None:
        if next_event == EVENT_TYPE.PLANET_ROTATION:
            planet_rotation(game, players, planets)
        elif next_event == EVENT_TYPE.OFFER_DEMAND:
            offer_demand(game, planets)
        next_event = get_next_event(game, players)
    game.save()
    active_player.save()

def compute_distance(coordinates1, coordinates2):
    absolute_distance = max(
        abs(coordinates1[0]-coordinates2[0]),
        abs(coordinates1[1]-coordinates2[1]),
        abs(coordinates1[0]+coordinates1[1]-coordinates2[0]-coordinates2[1])
    )
    return absolute_distance + 2

def get_next_event(game, players):
    planet_rotation_event = [game.planet_rotation_event_time, game.planet_rotation_event_move]
    offer_demand_event = [game.offer_demand_event_time, game.offer_demand_event_move]
    active_player = get_active_player(players)
    if is_before(planet_rotation_event, offer_demand_event):
        if is_before(planet_rotation_event, [active_player.time_spent, active_player.last_move]):
            return EVENT_TYPE.PLANET_ROTATION
    else:
        if is_before(offer_demand_event, [active_player.time_spent, active_player.last_move]):
            return EVENT_TYPE.OFFER_DEMAND

    return None

def planet_rotation(game, players, planets):
    """
    move planets and player positions which are located at planets
    increase event time
    set event move
    increase turn counter
    """
    game.planet_rotation_event_time = game.planet_rotation_event_time + 10
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
    time_increase = [40, 30, 25, 20]
    game.offer_demand_event_time = game.offer_demand_event_time + time_increase[game.number_of_players - 1]
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
    active_player = None
    for player in players:
        if active_player is None:
            active_player = player
            continue
        if player_is_before(player, active_player):
            active_player = player
    return active_player

def player_is_before(player1, player2):
    return is_before([player1.time_spent, player1.last_move], [player2.time_spent, player2.last_move])

def is_before(one, two):
    if one[0] < two[0] or (one[0] == two[0] and one[1] > two[1]):
        return True
    return False

def compute_points(game, player_number):
    result = 0
    planet_points = [5, 3, 2, 1]
    for planet_influence in game.planet_influence_track:
        current_player_influence = planet_influence[player_number - 1]
        if current_player_influence == 0:
            continue
        rated_higher = sum(i > current_player_influence for i in planet_influence)
        rated_same = sum(i == current_player_influence for i in planet_influence)       
        result = result + int(sum(planet_points[rated_higher : rated_higher + rated_same])/rated_same)

    return result