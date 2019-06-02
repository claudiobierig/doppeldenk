"""
Tests to check the correctness of the spacetrading.logic module
"""

import itertools
from django.contrib.auth.models import User
from django.test import TestCase
from spacetrading.models import Game
from spacetrading.models import Player
from spacetrading.models import Planet
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
        pass

    def test_is_before(self):
        self.assertTrue(move.is_before([0, 2], [10, 3]))
        self.assertFalse(move.is_before([10, 3], [0, 2]))
        self.assertTrue(move.is_before([10, 4], [10, 3]))
        self.assertFalse(move.is_before([10, 3], [10, 4]))

    def test_player_is_before(self):
        pass

    def test_planet_rotation(self):
        pass

    def test_offer_demand(self):
        pass

    def test_compute_points(self):
        pass

    def test_get_current_planet(self):
        pass

    def test_is_move_valid(self):
        pass

    def test_compute_trade_balance(self):
        pass

    def test_change_active_player(self):
        pass

    def test_change_active_planet(self):
        pass

    def test_change_game(self):
        pass

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
