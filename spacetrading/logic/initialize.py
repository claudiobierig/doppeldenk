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
    game = Game.objects.create_game(
        game_name=name,
        number_of_players=number_of_players,
        offer_demand_event_time=gamesettings.OFFER_DEMAND_EVENT_TIMES[number_of_players-1],
        resource_limit=resource_limit
    )
    b_resources = ['1', '2', '3', '4', '5']
    remaining_s_resources = ['1', '2', '3', '4', '5']
    s_resources = []
    random.shuffle(b_resources)

    for i in range(3):
        shuffle_resources = remaining_s_resources.copy()
        if b_resources[i] in shuffle_resources:
            shuffle_resources.remove(b_resources[i])
        random.shuffle(shuffle_resources)
        s_resources.append(shuffle_resources[0])
        remaining_s_resources.remove(shuffle_resources[0])
    if b_resources[3] == remaining_s_resources[0] or b_resources[4] == remaining_s_resources[1]:
        s_resources.append(remaining_s_resources[1])
        s_resources.append(remaining_s_resources[0])
    else:
        s_resources.append(remaining_s_resources[0])
        s_resources.append(remaining_s_resources[1])

    player = Player.objects.create_player(
        user=user,
        colour="#FF0000",
        ship_offset=[0, 0],
        player_number=0
    )
    game.players.add(player)    

    for index, current_planet in enumerate(gamesettings.PLANETS):
        planet = Planet.objects.create_planet(
            name=current_planet[0],
            colour=current_planet[2],
            number_of_hexes=current_planet[1],
            current_position=random.randint(0, current_planet[1] - 1),
            buy_resources=[b_resources[index], '0', '0', '0', '0'],
            cost_buy_resource=[
                random.randint(
                    gamesettings.SETUP_BUY_PRICE[0],
                    gamesettings.SETUP_BUY_PRICE[1]
                ), 0, 0, 0, 0
            ],
            sell_resources=[s_resources[index], '0', '0', '0', '0'],
            cost_sell_resource=[
                random.randint(
                    gamesettings.SETUP_SELL_PRICE[0],
                    gamesettings.SETUP_SELL_PRICE[1]
                ), 0, 0, 0, 0
            ],
            position_of_hexes=current_planet[3],
            radius_x=current_planet[4][0],
            radius_y=current_planet[4][1],
            offset=current_planet[5]
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
            current_player.money = 10 + game.number_of_players - current_player.player_number - 1
            current_player.save()
        game.game_state = 'r'
    elif number_of_joined_players > game.number_of_players - 1:
        game.players.remove(player)
        player.delete()

    game.save()
