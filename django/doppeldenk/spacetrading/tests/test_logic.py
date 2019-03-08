from django.test import TestCase
from spacetrading.models import Game
from spacetrading.models import Player
from spacetrading.models import Planet
from spacetrading.logic import move

# Create your tests here.

class MoveTest(TestCase):
    
    def setUp(self):
        self.game = Game.objects.create_game(
            game_name="test",
            number_of_players=2,
            game_state="r"
        )

        player1 = Player.objects.create_player(
            player_number=1,
            last_move=-1,
            time_spent=0
        )
        player2 = Player.objects.create_player(
            player_number=2,
            last_move=-2,
            time_spent=0
        )
        self.game.players.add(player1)
        self.game.players.add(player2)
        planet1 = Planet.objects.create_planet(
            name="a",
            number_of_hexes=3,
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
            cost_buy_resource=[3, 0, 0, 0, 0],
            sell_resources=['2', '0', '0', '0', '0'],
            cost_sell_resource=[5, 0, 0, 0, 0],
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
        player1 = self.players.get(player_number=1)
        player2 = self.players.get(player_number=2)
        player1.time_spent = 21
        player2.time_spent = 22
        player1.save()
        player2.save()
        self.players = self.game.players.all()
        self.assertEqual(move.EVENT_TYPE.PLANET_ROTATION, move.get_next_event(self.game, self.players))
        self.game.planet_rotation_event_time = 20
        self.game.planet_rotation_event_move = 1
        self.assertEqual(move.EVENT_TYPE.PLANET_ROTATION, move.get_next_event(self.game, self.players))
        self.game.planet_rotation_event_time = 30
        self.assertEqual(move.EVENT_TYPE.OFFER_DEMAND, move.get_next_event(self.game, self.players))
        
    def test_get_active_player(self):
        self.assertEqual(1, move.get_active_player(self.players).player_number)

    def test_is_before(self):
        self.assertTrue(move.is_before([0, 2], [10, 3]))
        self.assertFalse(move.is_before([10, 3], [0, 2]))
        self.assertTrue(move.is_before([10, 4], [10, 3]))
        self.assertFalse(move.is_before([10, 3], [10, 4]))

    def test_player_is_before(self):
        player1 = self.players.get(player_number=1)
        player2 = self.players.get(player_number=2)
        self.assertTrue(move.player_is_before(player1, player2))
        self.assertFalse(move.player_is_before(player2, player1))
        player1.time_spent = 10
        self.assertTrue(move.player_is_before(player2, player1))
        self.assertFalse(move.player_is_before(player1, player2))