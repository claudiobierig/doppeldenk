"""
Tests to check the correctness of the spacetrading.logic module
"""

import itertools
from django.contrib.auth.models import User
from django.test import TestCase
from spacetrading.models import Game
from spacetrading.logic import gamesettings
from spacetrading.logic import initialize
from spacetrading.logic import move

class MoveTest(TestCase):
    """
    Class for all tests of logic.move
    """

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1')
        number_of_players = 4
        game_name = "game_{}".format(number_of_players)
        data = {
            "name": game_name,
            "number_of_players": number_of_players,
            "play_all_players": True,
            "resource_limit": 5,
            "midgame_scoring": True
        }
        initialize.create_game(data, self.user1)
        games = Game.objects.filter(game_name=game_name)
        self.assertEqual(len(games), 1)
        self.game = games[0]
        self.players = self.game.players.all().order_by('player_number')
        self.planets = self.game.planets.all().order_by('planet_number')
        

    def test_distance(self):
        coord1 = [1, 1]
        coord2 = [-1, -1]
        coord3 = [-2, 2]
        self.assertEqual(6, move.compute_distance(coord1, coord2))
        self.assertEqual(5, move.compute_distance(coord2, coord3))
        self.assertEqual(5, move.compute_distance(coord1, coord3))

    def test_get_next_event(self):
        self.assertEqual(None, move.get_next_event(self.game, self.players))
        for player in self.players:
            player.time_spent = 10
            player.last_move = player.player_number
        self.assertEqual(None, move.get_next_event(self.game, self.players))
        for player in self.players:
            player.time_spent = 11
        self.assertEqual(move.Event.PLANET_ROTATION, move.get_next_event(self.game, self.players))
        move.planet_rotation(self.game, self.players, self.planets)
        self.assertEqual(move.Event.OFFER_DEMAND, move.get_next_event(self.game, self.players))
        move.offer_demand(self.game, self.planets)
        self.assertEqual(None, move.get_next_event(self.game, self.players))
        for player in self.players:
            player.time_spent = 21
        self.assertEqual(move.Event.OFFER_DEMAND, move.get_next_event(self.game, self.players))
        move.offer_demand(self.game, self.planets)
        self.assertEqual(move.Event.PLANET_ROTATION, move.get_next_event(self.game, self.players))
        move.planet_rotation(self.game, self.players, self.planets)

        for player in self.players:
            player.time_spent = 51
        self.assertEqual(move.Event.PLANET_ROTATION, move.get_next_event(self.game, self.players))
        move.planet_rotation(self.game, self.players, self.planets)
        self.assertEqual(move.Event.OFFER_DEMAND, move.get_next_event(self.game, self.players))
        move.offer_demand(self.game, self.planets)
        
        self.assertEqual(move.Event.OFFER_DEMAND, move.get_next_event(self.game, self.players))
        move.offer_demand(self.game, self.planets)
        self.assertEqual(move.Event.PLANET_ROTATION, move.get_next_event(self.game, self.players))
        move.planet_rotation(self.game, self.players, self.planets)

        self.assertEqual(move.Event.PLANET_ROTATION, move.get_next_event(self.game, self.players))
        move.planet_rotation(self.game, self.players, self.planets)
        self.assertEqual(move.Event.OFFER_DEMAND, move.get_next_event(self.game, self.players))
        move.offer_demand(self.game, self.planets)
        self.assertEqual(move.Event.MIDGAME_SCORING, move.get_next_event(self.game, self.players))
        move.midgame_scoring(self.game, self.players)
        self.assertEqual(None, move.get_next_event(self.game, self.players))

    def test_get_active_player(self):
        self.assertEqual(move.get_active_player(self.players), self.players[0])
        for player in self.players:
            player.time_spent = 0
            player.last_move = player.player_number + 1
        self.assertEqual(move.get_active_player(self.players), self.players[3])
        self.players[3].time_spent = 4
        self.assertEqual(move.get_active_player(self.players), self.players[2])
        for player in self.players:
            player.time_spent = 100
        self.assertEqual(move.get_active_player(self.players), self.players[3])
        self.players[3].time_spent = 101
        self.assertEqual(move.get_active_player(self.players), self.players[2])
        self.players[2].has_passed = True
        self.assertEqual(move.get_active_player(self.players), self.players[1])
        self.players[1].has_passed = True
        self.players[0].has_passed = True
        self.assertEqual(move.get_active_player(self.players), None)

    def test_is_before(self):
        self.assertTrue(move.is_before([0, 2], [10, 3]))
        self.assertFalse(move.is_before([10, 3], [0, 2]))
        self.assertTrue(move.is_before([10, 4], [10, 3]))
        self.assertFalse(move.is_before([10, 3], [10, 4]))

    def test_player_is_before(self):
        player1 = self.players[0]
        player2 = self.players[1]
        self.assertTrue(move.player_is_before(player1, player2))
        self.assertFalse(move.player_is_before(player2, player1))
        player1.time_spent = 0
        player1.last_move = 1
        self.assertTrue(move.player_is_before(player2, player1))
        self.assertFalse(move.player_is_before(player1, player2))
        player2.time_spent = 0
        player2.last_move = 2
        self.assertTrue(move.player_is_before(player2, player1))
        self.assertFalse(move.player_is_before(player1, player2))
        player2.time_spent = 4
        player2.last_move = 3
        self.assertTrue(move.player_is_before(player1, player2))
        self.assertFalse(move.player_is_before(player2, player1))
        player1.has_passed = True
        self.assertTrue(move.player_is_before(player2, player1))
        self.assertFalse(move.player_is_before(player1, player2))
        player2.has_passed = True
        self.assertFalse(move.player_is_before(player1, player2))
        self.assertFalse(move.player_is_before(player2, player1))

    def test_planet_rotation(self):
        starting_position = []
        for planet in self.planets:
            starting_position.append(planet.current_position)
        player1 = self.players[0]
        player1.ship_position = self.planets[0].position_of_hexes[self.planets[0].current_position]
        player1.save()
        player2 = self.players[1]
        player2.ship_position = [0, 0]
        player2.save()
        for i in range(14):
            move.planet_rotation(self.game, self.players, self.planets)
            self.assertEqual(self.planets[0].position_of_hexes[self.planets[0].current_position], self.players[0].ship_position)
            self.assertEqual([0, 0], self.players[1].ship_position)
            for planet in self.planets:
                self.assertEqual(planet.current_position, (starting_position[planet.planet_number] + i + 1) % planet.number_of_hexes)

    def get_prices(self, planets):
        return {
            planet.name : (planet.cost_buy_resource[0], planet.cost_sell_resource[0])
                for planet in planets
        }

    def test_offer_demand(self):
        old_prices = self.get_prices(self.planets)
        for i in range(5):
            move.offer_demand(self.game, self.planets)
            new_prices = self.get_prices(self.planets)
            for key, (buy_price, sell_price) in old_prices.items():
                self.assertEqual(new_prices[key][0], max(buy_price - 1, 1))
                self.assertEqual(new_prices[key][1], min(sell_price + 1, 7))
            old_prices = new_prices
            self.assertEqual(self.game.offer_demand_event_move, i+1)
            self.assertEqual(self.game.offer_demand_event_time, (i+2)*gamesettings.OFFER_DEMAND_EVENT_TIMES[self.game.number_of_players - 1])

    def test_midgame_scoring(self):
        self.game.planet_influence_track = [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 1, 0],
            [3, 1, 1, 0]
        ]
        move.midgame_scoring(self.game, self.players)
        self.assertEqual(self.players[0].points, 6)
        self.assertEqual(self.players[1].points, 2)
        self.assertEqual(self.players[2].points, 1)
        self.assertEqual(self.players[3].points, 0)
        self.assertEqual(self.game.midgame_scoring_event_move, 1)
        self.assertEqual(self.game.midgame_scoring_event_time, 2*gamesettings.MIDGAME_SCORING_TIME)

    def test_compute_points(self):
        self.game.planet_influence_track = [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 1, 0],
            [3, 1, 1, 0]
        ]
        points = [move.compute_points(self.game, player) for player in self.players]
        self.assertEqual(points, [17, 9, 5, 0])
        for player in self.players:
            player.points = 1
        points = [move.compute_points(self.game, player) for player in self.players]
        self.assertEqual(points, [18, 10, 6, 1])
        points = [move.compute_points(self.game, player, [2, 1]) for player in self.players]
        self.assertEqual(points, [7, 3, 2, 1])

    def test_get_active_planet(self):
        planet_positions = [(planet.position_of_hexes[planet.current_position], planet) for planet in self.planets]
        for position, planet in planet_positions:
            self.assertEqual(planet, move.get_active_planet(position, self.planets))
        self.assertEqual(None, move.get_active_planet([0, 0], self.planets))
    
    def test_get_cost_influence(self):
        self.assertEqual(0, move.get_cost_influence(True, 0, 0))
        self.assertEqual(0, move.get_cost_influence(False, 0, 0))
        self.assertEqual(0, move.get_cost_influence(True, 0, 10))
        self.assertEqual(1, move.get_cost_influence(True, 1, 5))
        self.assertEqual(6, move.get_cost_influence(False, 1, 5))
        self.assertEqual(8, move.get_cost_influence(True, 2, 5))
        self.assertEqual(13, move.get_cost_influence(False, 2, 5))
        self.assertEqual(16, move.get_cost_influence(True, 3, 5))
        self.assertEqual(21, move.get_cost_influence(False, 3, 5))

    def test_get_trade_balance_or_raise(self):
        data = {
            'coord_q': 0,
            'coord_r': 0
        }
        active_player = move.get_active_player(self.players)
        active_planet = move.get_active_planet(active_player.ship_position, self.planets)
        with self.assertRaises(move.MoveError):
            move.get_trade_balance_or_raise(active_player, active_planet, self.game, data)
        with self.assertRaises(move.MoveError):
            move.get_trade_balance_or_raise(active_player, active_planet, self.game, {})
        data = {
            'coord_q': 1,
            'coord_r': 1
        }
        self.assertEqual(0, move.get_trade_balance_or_raise(active_player, active_planet, self.game, data))
        for i, _ in enumerate(self.players):
            active_player = move.get_active_player(self.players)
            active_planet = move.get_active_planet(active_player.ship_position, self.planets)
            data = {
                'coord_q': self.planets[i].position_of_hexes[self.planets[i].current_position][0],
                'coord_r': self.planets[i].position_of_hexes[self.planets[i].current_position][1]
            }
            move.move(self.game, data)
            self.players = self.game.players.all().order_by('player_number')
            self.planets = self.game.planets.all().order_by('planet_number')

        active_player = move.get_active_player(self.players)
        active_planet = move.get_active_planet(active_player.ship_position, self.planets)
        data = {
            'coord_q': active_player.ship_position[0],
            'coord_r': active_player.ship_position[1]
        }

        with self.assertRaises(move.MoveError):
            move.get_trade_balance_or_raise(active_player, active_planet, self.game, data)
        data['spend_time'] = 3
        with self.assertRaises(move.MoveError):
            move.get_trade_balance_or_raise(active_player, active_planet, self.game, data)
        data['spend_time'] = 4
        self.assertEqual(0, move.get_trade_balance_or_raise(active_player, active_planet, self.game, data))
        data[move.BUY_MAPPING[active_planet.buy_resources[0]]] = self.game.resource_limit + 1
        with self.assertRaises(move.MoveError):
            move.get_trade_balance_or_raise(active_player, active_planet, self.game, data)
        data[move.BUY_MAPPING[active_planet.buy_resources[0]]] = 1
        self.assertEqual(-active_planet.cost_buy_resource[0], move.get_trade_balance_or_raise(active_player, active_planet, self.game, data))
        data['buy_influence'] = 1
        self.assertEqual(-active_planet.cost_buy_resource[0] - 1, move.get_trade_balance_or_raise(active_player, active_planet, self.game, data))
        data['buy_influence'] = 5
        with self.assertRaises(move.MoveError):
            move.get_trade_balance_or_raise(active_player, active_planet, self.game, data)
        data['buy_influence'] = 0
        data[move.SELL_MAPPING[active_planet.sell_resources[0]]] = 2
        with self.assertRaises(move.MoveError):
            move.get_trade_balance_or_raise(active_player, active_planet, self.game, data)
        active_player.resources[int(active_planet.sell_resources[0]) - 1] = 2
        self.assertEqual(-active_planet.cost_buy_resource[0] + 2*active_planet.cost_sell_resource[0], \
            move.get_trade_balance_or_raise(active_player, active_planet, self.game, data))
        with self.assertRaises(move.MoveError):
            move.get_trade_balance_or_raise(None, None, self.game, {})
        self.assertEqual('f', self.game.game_state)

    def test_change_active_player_startup(self):
        active_player = move.get_active_player(self.players)
        active_planet = move.get_active_planet(active_player.ship_position, self.planets)
        data = {
            'coord_q': 1,
            'coord_r': 1
        }
        move.change_active_player(active_player, active_planet, 1, data, 0)
        self.players = self.game.players.all().order_by('player_number')
        player = self.players[0]
        self.assertEqual(player.ship_position, [1, 1])
        self.assertEqual(player.time_spent, 0)
        self.assertEqual(player.last_move, 1)

    def test_change_active_player_normal_move(self):
        for i, _ in enumerate(self.players):
            active_player = move.get_active_player(self.players)
            active_planet = move.get_active_planet(active_player.ship_position, self.planets)
            data = {
                'coord_q': self.planets[i].position_of_hexes[self.planets[i].current_position][0],
                'coord_r': self.planets[i].position_of_hexes[self.planets[i].current_position][1]
            }
            move.move(self.game, data)
            self.players = self.game.players.all().order_by('player_number')
            self.planets = self.game.planets.all().order_by('planet_number')
        
        active_player = move.get_active_player(self.players)
        active_planet = move.get_active_planet(active_player.ship_position, self.planets)
        data = {
            'coord_q': 1,
            'coord_r': 1,
            'spend_time': 50,
            move.BUY_MAPPING[active_planet.buy_resources[0]]: 1,
            move.BUY_MAPPING[active_planet.sell_resources[0]]: 0
        }
        trade_balance = 17
        next_move = 18
        move.change_active_player(active_player, active_planet, next_move, data, trade_balance)
        self.players = self.game.players.all().order_by('player_number')
        
        player = self.players[3]
        self.assertEqual(player.ship_position, [1, 1])
        self.assertEqual(player.time_spent, 50)
        self.assertEqual(player.last_move, next_move)
        self.assertEqual(player.resources[int(active_planet.buy_resources[0]) - 1], 1)
        self.assertEqual(player.money, 10 + trade_balance)

    def test_change_active_planet(self):
        for i, _ in enumerate(self.players):
            active_player = move.get_active_player(self.players)
            active_planet = move.get_active_planet(active_player.ship_position, self.planets)
            data = {
                'coord_q': self.planets[i].position_of_hexes[self.planets[i].current_position][0],
                'coord_r': self.planets[i].position_of_hexes[self.planets[i].current_position][1]
            }
            move.move(self.game, data)
            self.players = self.game.players.all().order_by('player_number')
            self.planets = self.game.planets.all().order_by('planet_number')
        
        active_player = move.get_active_player(self.players)
        active_planet = move.get_active_planet(active_player.ship_position, self.planets)
        old_prices = self.get_prices([active_planet])

        for i in range(5):
            data = {
                move.BUY_MAPPING[active_planet.buy_resources[0]]: 1,
                move.SELL_MAPPING[active_planet.sell_resources[0]]: 1
            }
            move.change_active_planet(active_planet, data)
            new_prices = self.get_prices([active_planet])
            for key, (buy_price, sell_price) in old_prices.items():
                self.assertEqual(new_prices[key][0], min(buy_price + 1, 6))
                self.assertEqual(new_prices[key][1], max(sell_price - 1, 2))
            old_prices = new_prices
            
    def test_change_game(self):
        move.change_game(self.game, self.players, self.planets, None, 0, {})
        self.assertEqual(self.game.next_move_number, 2)
        for i, _ in enumerate(self.players):
            data = {
                'coord_q': self.planets[i].position_of_hexes[self.planets[i].current_position][0],
                'coord_r': self.planets[i].position_of_hexes[self.planets[i].current_position][1]
            }
            move.move(self.game, data)
            self.planets = self.game.planets.all().order_by('planet_number')
        self.players = self.game.players.all().order_by('player_number')

        active_player = move.get_active_player(self.players)
        active_planet = move.get_active_planet(active_player.ship_position, self.planets)
        data = {'buy_influence': 5}
        move.change_game(self.game, self.players, self.planets, active_planet, active_player.player_number, data)
        self.assertEqual(self.game.next_move_number, 7)
        self.assertEqual(self.game.planet_influence_track[active_planet.planet_number][active_player.player_number], 5)
        for player in self.players:
            player.time_spent = 11
        move.change_game(self.game, self.players, self.planets, active_planet, active_player.player_number, data)
        self.assertEqual(self.game.next_move_number, 10)
        self.assertEqual(self.game.planet_influence_track[active_planet.planet_number][active_player.player_number], 10)
        self.assertEqual(self.game.planet_rotation_event_time, 20)
        self.assertEqual(self.game.planet_rotation_event_move, 8)
        self.assertEqual(self.game.offer_demand_event_time, 20)
        self.assertEqual(self.game.offer_demand_event_move, 9)

class InitializeTest(TestCase):
    """
    Test class for initialize module
    """
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1')

    def test_it_creates_games_as_configured(self):
        """
        for all combined_possibilities generate a game and see if all is setup correctly
        skip test for joining, since we use the join method if play_all_players is True
        """
        possibilities = {
            "number_of_players": range(1, 5),
            "play_all_players": [False, True],
            "resource_limit": [5, 9],
            "midgame_scoring": [False, True]
        }
        combined_possibilities = itertools.product(
            possibilities["number_of_players"],
            possibilities["play_all_players"],
            possibilities["resource_limit"],
            possibilities["midgame_scoring"]
        )

        for index, (number_of_players, play_all_players, resource_limit, midgame_scoring) in \
            enumerate(combined_possibilities):
            game_name = "test_{}".format(index)
            data = {
                "name": game_name,
                "number_of_players": number_of_players,
                "play_all_players": play_all_players,
                "resource_limit": resource_limit,
                "midgame_scoring": midgame_scoring
            }
            initialize.create_game(data, self.user1)
            games = Game.objects.filter(game_name=game_name)
            self.assertEqual(len(games), 1)
            game = games[0]
            players = game.players.all().order_by('player_number')
            planets = game.planets.all().order_by('planet_number')
            self.assertEqual(len(planets), 5)

            self.assertEqual(game.number_of_players, number_of_players)
            if play_all_players:
                self.assertEqual(len(players), number_of_players)
            else:
                self.assertEqual(len(players), 1)
                self.assertEqual(players[0].user, self.user1)

            if play_all_players or number_of_players == 1:
                self.assertEqual(game.game_state, 'r')
                for index_player, player in enumerate(players):
                    self.assertEqual(player.user, self.user1)
                    self.assertEqual(index_player, player.player_number)
                    self.assertEqual(player.last_move, -player.player_number -1)
                    self.assertEqual(player.money, 9 + number_of_players - player.player_number)
                    self.assertEqual(player.resources, [0, 0, 0, 0, 0])
                    self.assertEqual(player.time_spent, -1)
                    self.assertEqual(player.points, 0)
                    self.assertFalse(player.has_passed)
            else:
                self.assertEqual(game.game_state, 'w')

            self.assertEqual(game.resource_limit, resource_limit)
            self.assertEqual(game.midgame_scoring, midgame_scoring)
            if midgame_scoring:
                self.assertEqual(game.midgame_scoring_event_move, gamesettings.MIDGAME_SCORING_MOVE)
                self.assertEqual(game.midgame_scoring_event_time, gamesettings.MIDGAME_SCORING_TIME)

            self.assertEqual(game.planet_rotation_event_move, gamesettings.PLANET_ROTATION_MOVE)
            self.assertEqual(game.planet_rotation_event_time, gamesettings.PLANET_ROTATION_TIME)
            self.assertEqual(game.offer_demand_event_move, gamesettings.OFFER_DEMAND_EVENT_MOVE)
            self.assertEqual(game.offer_demand_event_time, gamesettings.OFFER_DEMAND_EVENT_TIMES[number_of_players - 1])

            self.assertEqual(game.next_move_number, gamesettings.FIRST_MOVE_NUMBER)
            self.assertEqual(game.planet_influence_track, [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ])

            buy_resources = []
            sell_resources = []
            for index_planet, planet in enumerate(planets):
                self.assertEqual(index_planet, planet.planet_number)
                self.assertEqual(planet.name, gamesettings.PLANETS[planet.planet_number][0])
                self.assertEqual(planet.colour, gamesettings.PLANETS[planet.planet_number][2])
                self.assertEqual(planet.number_of_hexes, gamesettings.PLANETS[planet.planet_number][1])
                self.assertEqual(planet.position_of_hexes, gamesettings.PLANETS[planet.planet_number][3])
                self.assertLess(planet.current_position, planet.number_of_hexes)
                self.assertGreaterEqual(planet.current_position, 0)

                self.assertGreaterEqual(planet.cost_buy_resource[0], gamesettings.SETUP_BUY_PRICE[0])
                self.assertLessEqual(planet.cost_buy_resource[0], gamesettings.SETUP_BUY_PRICE[1])
                
                buy_resources.append(planet.buy_resources[0])
                sell_resources.append(planet.sell_resources[0])
                self.assertNotEqual(planet.buy_resources[0], planet.sell_resources[0])
                self.assertGreaterEqual(planet.cost_sell_resource[0], gamesettings.SETUP_SELL_PRICE[0])
                self.assertLessEqual(planet.cost_sell_resource[0], gamesettings.SETUP_SELL_PRICE[1])
                for i in range(1, 5):
                    self.assertEqual(planet.buy_resources[i], '0')
                    self.assertEqual(planet.sell_resources[i], '0')

            self.assertEqual(sorted(buy_resources), ['1', '2', '3', '4', '5'])
            self.assertEqual(sorted(sell_resources), ['1', '2', '3', '4', '5'])
