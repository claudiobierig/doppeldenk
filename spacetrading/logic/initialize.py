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
    finish_time = data.get('finish_time', gamesettings.FINISH_TIME)
    start_influence = data.get('start_influence', gamesettings.START_INFLUENCE)
    game = Game.objects.create_game(
        game_name=name,
        number_of_players=number_of_players,
        offer_demand_event_time=gamesettings.OFFER_DEMAND_EVENT_TIMES[number_of_players-1],
        resource_limit=resource_limit,
        midgame_scoring=midgame_scoring,
        midgame_scoring_event_time=finish_time/2,
        finish_time=finish_time,
        start_influence=start_influence
    )
    demand_resources = ['1', '5', '2', '3', '4']
    remaining_supply_resources = {'1', '2', '3', '4', '5'}
    supply_resources = []
    for i in range(3):
        demand_resource = random.sample(remaining_supply_resources - set(demand_resources[i]), 1)[0]
        remaining_supply_resources.remove(demand_resource)
        supply_resources.append(demand_resource)

    remaining_supply_resources = list(remaining_supply_resources)
    random.shuffle(remaining_supply_resources)
    if demand_resources[3] is remaining_supply_resources[0] or demand_resources[4] is remaining_supply_resources[1]:
        supply_resources.append(remaining_supply_resources[1])
        supply_resources.append(remaining_supply_resources[0])
    else:
        supply_resources.append(remaining_supply_resources[0])
        supply_resources.append(remaining_supply_resources[1])

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

    for index, current_planet in enumerate(gamesettings.PLANETS):
        planet = Planet.objects.create_planet(
            name=current_planet[0],
            colour=current_planet[2],
            number_of_hexes=current_planet[1],
            current_position=random.randint(0, current_planet[1] - 1),
            planet_demand_resource=demand_resources[index],
            planet_demand_resource_price=demand_prices[index],
            planet_supply_resource=supply_resources[index],
            planet_supply_resource_price=supply_prices[index],
            position_of_hexes=current_planet[3],
            radius_x=current_planet[4][0],
            radius_y=current_planet[4][1],
            offset=current_planet[5],
            planet_number=index
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
