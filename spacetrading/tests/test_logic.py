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
        self.game = Game.objects.create_game(
            game_name="test",
            number_of_players=2,
            game_state="r",
            offer_demand_event_time=20
        )

        player1 = Player.objects.create_player(
            player_number=0,
            last_move=-1,
            time_spent=0
        )
        player2 = Player.objects.create_player(
            player_number=1,
            last_move=-2,
            time_spent=0
        )
        self.game.players.add(player1)
        self.game.players.add(player2)
        planet1 = Planet.objects.create_planet(
            name="a",
            number_of_hexes=3,
            current_position=0,
            buy_resources=['1', '0', '0', '0', '0'],
            cost_buy_resource=[3, 0, 0, 0, 0],
            sell_resources=['2', '0', '0', '0', '0'],
            cost_sell_resource=[5, 0, 0, 0, 0],
            position_of_hexes=[[1, 1], [2, 2], [3, 3]]
        )
        planet2 = Planet.objects.create_planet(
            name="b",
            number_of_hexes=5,
            current_position=3,
            buy_resources=['1', '0', '0', '0', '0'],
            cost_buy_resource=[1, 0, 0, 0, 0],
            sell_resources=['2', '0', '0', '0', '0'],
            cost_sell_resource=[7, 0, 0, 0, 0],
            position_of_hexes=[[-2, 2], [-3, -3], [4, 4], [5, -5], [-6, 6]]
        )
        self.game.planets.add(planet1)
        self.game.planets.add(planet2)
        self.players = self.game.players.all()
        self.planets = self.game.planets.all()

    def test_setup(self):
        self.assertEqual(2, self.game.planets.count())
        self.assertEqual(2, self.game.players.count())

    def test_distance(self):
        coord1 = [1, 1]
        coord2 = [-1, -1]
        coord3 = [-2, 2]
        self.assertEqual(6, move.compute_distance(coord1, coord2))
        self.assertEqual(5, move.compute_distance(coord2, coord3))
        self.assertEqual(5, move.compute_distance(coord1, coord3))

    def test_get_next_event(self):
        self.assertEqual(None, move.get_next_event(self.game, self.players))
        player1 = self.players.get(player_number=0)
        player2 = self.players.get(player_number=1)
        player1.time_spent = 31
        player2.time_spent = 32
        player1.save()
        player2.save()
        self.players = self.game.players.all()
        self.assertEqual(move.Event.PLANET_ROTATION,
                         move.get_next_event(self.game, self.players))
        self.game.planet_rotation_event_time = 20
        self.game.planet_rotation_event_move = 1
        self.assertEqual(move.Event.PLANET_ROTATION,
                         move.get_next_event(self.game, self.players))
        self.game.planet_rotation_event_time = 40
        self.assertEqual(move.Event.OFFER_DEMAND,
                         move.get_next_event(self.game, self.players))

    def test_get_active_player(self):
        self.assertEqual(0, move.get_active_player(self.players).player_number)

    def test_is_before(self):
        self.assertTrue(move.is_before([0, 2], [10, 3]))
        self.assertFalse(move.is_before([10, 3], [0, 2]))
        self.assertTrue(move.is_before([10, 4], [10, 3]))
        self.assertFalse(move.is_before([10, 3], [10, 4]))

    def test_player_is_before(self):
        player1 = self.players.get(player_number=0)
        player2 = self.players.get(player_number=1)
        self.assertTrue(move.player_is_before(player1, player2))
        self.assertFalse(move.player_is_before(player2, player1))
        player1.time_spent = 10
        self.assertTrue(move.player_is_before(player2, player1))
        self.assertFalse(move.player_is_before(player1, player2))

    def test_planet_rotation(self):
        move.planet_rotation(self.game, self.players, self.planets)
        position = self.get_current_planet_positions()
        self.assertTrue(position == [1, 4])
        self.assertEqual(2, self.game.next_move_number)
        self.assertEqual(1, self.game.planet_rotation_event_move)
        self.assertEqual(20, self.game.planet_rotation_event_time)
        move.planet_rotation(self.game, self.players, self.planets)
        position = self.get_current_planet_positions()
        self.assertTrue(position == [2, 0])
        player1 = self.players.get(player_number=0)
        player2 = self.players.get(player_number=1)
        planet1 = self.planets.get(name="a")
        planet2 = self.planets.get(name="b")
        player1.ship_position = planet1.position_of_hexes[planet1.current_position]
        player2.ship_position = planet2.position_of_hexes[planet2.current_position]
        player1.save()
        player2.save()
        self.players = self.game.players.all()
        move.planet_rotation(self.game, self.players, self.planets)
        player1 = self.players.get(player_number=0)
        player2 = self.players.get(player_number=1)
        self.assertTrue(player1.ship_position == planet1.position_of_hexes[0])
        self.assertTrue(player2.ship_position == planet2.position_of_hexes[1])

    def get_current_planet_positions(self):
        planet1 = self.planets.get(name="a")
        planet2 = self.planets.get(name="b")
        return [planet1.current_position, planet2.current_position]

    def test_offer_demand(self):
        move.offer_demand(self.game, self.planets)
        self.assertEqual(2, self.game.next_move_number)
        self.assertEqual(1, self.game.offer_demand_event_move)
        self.assertEqual(40, self.game.offer_demand_event_time)
        planet1 = self.planets.get(name="a")
        planet2 = self.planets.get(name="b")
        self.assertEqual(2, planet1.cost_buy_resource[0])
        self.assertEqual(6, planet1.cost_sell_resource[0])
        self.assertEqual(1, planet2.cost_buy_resource[0])
        self.assertEqual(7, planet2.cost_sell_resource[0])

    def test_compute_points(self):
        self.game.planet_influence_track = [
            [0, 1, 2, 3],
            [1, 1, 2, 2],
            [0, 0, 0, 0],
            [2, 1, 1, 1],
            [1, 1, 0, 0]
        ]
        player1 = self.players.get(player_number=0)
        player2 = self.players.get(player_number=1)
        player3 = Player.objects.create_player(
            player_number=2,
            last_move=-1,
            time_spent=0
        )
        player4 = Player.objects.create_player(
            player_number=3,
            last_move=-1,
            time_spent=0
        )
        self.assertEqual(10, move.compute_points(self.game, player1))
        self.assertEqual(9, move.compute_points(self.game, player2))
        self.assertEqual(9, move.compute_points(self.game, player3))
        self.assertEqual(11, move.compute_points(self.game, player4))


"""
    def test_get_current_planet(self):
        self.assertFalse(True)

    def test_is_move_valid(self):
        self.assertFalse(True)

    def test_compute_trade_balance(self):
        self.assertFalse(True)

    def test_change_active_player(self):
        self.assertFalse(True)

    def test_change_active_planet(self):
        self.assertFalse(True)

    def test_change_game(self):
        self.assertFalse(True)
"""

class InitializeTest(TestCase):
    """
    Test class for initialize module
    """
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1')
        self.user2 = User.objects.create_user(username='user2', password='user2')
        self.user3 = User.objects.create_user(username='user3', password='user3')
        self.user4 = User.objects.create_user(username='user4', password='user4')

    def test_it_creates_games_as_configured(self):
        """
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
