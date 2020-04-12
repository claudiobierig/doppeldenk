"""
Business logic how to
- create a game
- join a game
"""

import random

from spacetrading.logic import gamesettings
from spacetrading.models import Game, Player, Planet


def create_game(data, user):
    """
    create a game with
    - name (string)
    - 1 <= number_of_players <= 4
    - play_all_players (bool)
    - user (Django user)
    """

    name = data['name']
    number_of_players = data['number_of_players']
    play_all_players = data['play_all_players']
    resource_limit = data['resource_limit']
    midgame_scoring = data.get('midgame_scoring', False)
    add_demand = data.get('add_demand', False)
    finish_time = data.get('finish_time', gamesettings.FINISH_TIME)
    start_influence = data.get('start_influence', gamesettings.START_INFLUENCE)
    game = Game.objects.create_game(
        game_name=name,
        number_of_players=number_of_players,
        offer_demand_event_time=gamesettings.OFFER_DEMAND_EVENT_TIMES[number_of_players-1],
        resource_limit=resource_limit,
        midgame_scoring=midgame_scoring,
        midgame_scoring_event_time=finish_time/2,
        add_demand=add_demand,
        finish_time=finish_time,
        start_influence=start_influence
    )
    supply_resources = ['2', '5', '1', '3', '4']
    remaining_demand_resources = {'1', '2', '3', '4', '5'}
    remaining_add_demand_resources = {'1', '2', '3', '4', '5'}
    demand_resources = []
    add_demand_resources = ['0', '0', '0', '0', '0']
    for i in range(3):
        demand_resource = random.sample(remaining_demand_resources - set(supply_resources[i]), 1)[0]
        remaining_demand_resources.remove(demand_resource)
        demand_resources.append(demand_resource)

    remaining_demand_resources = list(remaining_demand_resources)
    random.shuffle(remaining_demand_resources)
    if supply_resources[3] is remaining_demand_resources[0] or supply_resources[4] is remaining_demand_resources[1]:
        demand_resources.append(remaining_demand_resources[1])
        demand_resources.append(remaining_demand_resources[0])
    else:
        demand_resources.append(remaining_demand_resources[0])
        demand_resources.append(remaining_demand_resources[1])

    traded_resources = [[{supply_resources[i], demand_resources[i]}, i, 2] for i in range(5)]
    random.shuffle(traded_resources)
    for i in range(5):
        remaining_counted = [
            (
                resource,
                sum([resource in s[0] for s in traded_resources])
            ) for resource in remaining_add_demand_resources
        ]
        remaining_counted.sort(key=lambda tup: (-tup[1]))
        first = remaining_counted[0][0]
        traded_resources.sort(key=lambda tup: (-tup[2]))
        for element in traded_resources:
            if first not in element[0]:
                add_demand_resources[element[1]] = first
                remaining_add_demand_resources.remove(first)
                traded_resources.remove(element)
                for leftover in traded_resources:
                    leftover[2] = len(leftover[0] & remaining_add_demand_resources)
                break

    player = Player.objects.create_player(
        user=user,
        colour="#FF0000",
        ship_offset=[0, 0],
        player_number=0
    )
    game.players.add(player)

    supply_prices = random.sample(
        gamesettings.SETUP_PLANET_SUPPLY_PRICE,
        len(gamesettings.SETUP_PLANET_SUPPLY_PRICE)
    )
    demand_prices = random.sample(
        gamesettings.SETUP_PLANET_DEMAND_PRICE,
        len(gamesettings.SETUP_PLANET_DEMAND_PRICE)
    )
    add_demand_resource_time = [i*gamesettings.ADD_DEMAND_TIME for i in range(1, 6)]
    random.shuffle(add_demand_resource_time)

    for index, current_planet in enumerate(gamesettings.PLANETS):
        planet = Planet.objects.create_planet(
            name=current_planet[0],
            colour=current_planet[2],
            number_of_hexes=current_planet[1],
            current_position=random.randint(0, current_planet[1] - 1),
            planet_demand_resources=[demand_resources[index], '0', '0', '0', '0'],
            planet_demand_resources_price=[
                demand_prices[2*index], 0, 0, 0, 0
            ],
            planet_supply_resources=[supply_resources[index], '0', '0', '0', '0'],
            planet_supply_resources_price=[
                supply_prices[index], 0, 0, 0, 0
            ],
            position_of_hexes=current_planet[3],
            radius_x=current_planet[4][0],
            radius_y=current_planet[4][1],
            offset=current_planet[5],
            planet_number=index,
            add_demand_resource=add_demand_resources[index],
            add_demand_resource_price=demand_prices[2*index + 1],
            add_demand_resource_time=add_demand_resource_time[index]
        )
        game.planets.add(planet)

    if number_of_players == 1:
        game.game_state = 'r'
    game.save()
    player.save()
    if play_all_players:
        for _ in range(number_of_players - 1):
            join_game(game.id, user)


def join_game(primary_key_game, user):
    """
    join an open game
    - primary_key_game is the id of the game we want to join
    - user is the Django user which wants to join
    """
    game = Game.objects.get(pk=primary_key_game)
    number_of_joined_players = game.players.count()
    if number_of_joined_players >= game.number_of_players or number_of_joined_players > 3:
        return

    colours = ["#FF0000", "#0000FF", "#FFFFFF", "#00FF00"]
    offsets = [[0, 0], [-10, 0], [-10, -15], [0, -15]]
    player = Player.objects.create_player(
        user=user,
        colour=colours[number_of_joined_players],
        ship_offset=offsets[number_of_joined_players],
        player_number=number_of_joined_players
    )
    game.players.add(player)

    if number_of_joined_players == game.number_of_players - 1:
        players = game.players.all()
        player_numbers = list(range(len(players)))
        random.shuffle(player_numbers)
        for index, current_player in enumerate(players):
            current_player.player_number = player_numbers[index]
            current_player.last_move = -current_player.player_number - 1
            current_player.money = 10 + game.number_of_players - \
                current_player.player_number - 1
            current_player.save()
        game.game_state = 'r'
    elif number_of_joined_players > game.number_of_players - 1:
        game.players.remove(player)
        player.delete()

    game.save()
