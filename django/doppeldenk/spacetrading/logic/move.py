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
    pass

def offer_demand(game, planets):
    """
    adjust offer_demand prices
    increase event time
    set event move
    increase turn counter
    """
    pass

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