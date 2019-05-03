"""
Business logic how to
- create a game
- join a game
"""

import random

from spacetrading.models import Game, Player, Planet

def create_game(name, number_of_players, play_all_players, user):
    """
    create a game with
    - name (string)
    - 1 <= number_of_players <= 4
    - play_all_players (bool)
    - user (Django user)
    """
    offer_demand_event_times = [40, 30, 25, 20]
    game = Game.objects.create_game(
        game_name=name,
        number_of_players=number_of_players,
        offer_demand_event_time=offer_demand_event_times[number_of_players-1]
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

    min_buy_price = 2
    max_buy_price = 4
    min_sell_price = 4
    max_sell_price = 6

    player = Player.objects.create_player(
        user=user,
        colour="#FF0000",
        ship_offset=[0, 0],
        player_number=0
    )
    game.players.add(player)
    planets = [
        [
            "alpha",
            3,
            "#FF0000",
            [[5, -2], [-3, 4], [-3, -1]],
            [150, 100],
            0
        ],
        [
            "beta",
            5,
            "#FF8000",
            [[7, -3], [1, 3], [-6, 5], [-5, 0], [3, -5]],
            [210, 130],
            0.2
        ],
        [
            "gamma",
            7,
            "#FFFF00",
            [[8, -2], [2, 4], [-5, 7], [-9, 5], [-6, -1], [2, -6], [7, -6]],
            [260, 180],
            0.4
        ],
        [
            "delta",
            11,
            "#008000",
            [[9, -1], [4, 4], [-2, 7], [-7, 8], [-10, 7], [-10, 3], [-7, -1],
             [-1, -6], [5, -8], [9, -8], [11, -5]],
            [320, 210],
            0.6
        ],
        [
            "epsilon",
            13,
            "#1E90FF",
            [[8, 1], [3, 5], [-2, 8], [-8, 9], [-11, 8], [-12, 5], [-11, 2],
             [-6, -3], [0, -7], [5, -9], [10, -9], [12, -7], [12, -4]],
            [370, 240],
            0.8
        ]
    ]

    for index, current_planet in enumerate(planets):
        planet = Planet.objects.create_planet(
            name=current_planet[0],
            colour=current_planet[2],
            number_of_hexes=current_planet[1],
            current_position=random.randint(0, current_planet[1] - 1),
            buy_resources=[b_resources[index], '0', '0', '0', '0'],
            cost_buy_resource=[random.randint(min_buy_price, max_buy_price), 0, 0, 0, 0],
            sell_resources=[s_resources[index], '0', '0', '0', '0'],
            cost_sell_resource=[random.randint(min_sell_price, max_sell_price), 0, 0, 0, 0],
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
