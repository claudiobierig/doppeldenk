from django.test import TestCase
from spacetrading.models import Game
from spacetrading.models import Player
from spacetrading.models import Planet
from spacetrading.logic import move

# Create your tests here.

class YourTestClass(TestCase):
    
    def setUp(self):
        print("every test")
        game = Game.objects.create_game(
            game_name="test",
            number_of_players=2,
            game_state="r"
        )

        player1 = Player.objects.create_player(
            player_number=1
        )
        player2 = Player.objects.create_player(
            player_number=2
        )
        game.players.add(player1)
        game.players.add(player2)
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
        game.planets.add(planet1)
        game.planets.add(planet2)

    @classmethod
    def setUpTestData(cls):
        print("once on startup")
        pass

    def test_setup(self):
        game = Game.objects.get(game_name="test")
        self.assertEqual(2, game.planets.count())
        self.assertEqual(2, game.players.count())
    
    def test_distance(self):
        #TODO: move to different class
        coord1 = [1, 1]
        coord2 = [-1, -1]
        coord3 = [-2, 2]
        self.assertEqual(6, move.compute_distance(coord1, coord2))
        self.assertEqual(5, move.compute_distance(coord2, coord3))
        self.assertEqual(5, move.compute_distance(coord1, coord3))

    def test_get_next_event(self):
        game = Game.objects.get(game_name="test")
        players = game.players.all()
        self.assertEqual(None, move.get_next_event(game, players))
        #TODO: more tests
        self.assertTrue(False)
    
    def test_get_active_player(self):
        self.assertTrue(False)

    def test_is_before(self):
        self.assertTrue(False)

    def test_player_is_before(self):
        self.assertTrue(False)