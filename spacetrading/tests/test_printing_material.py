from django.test import TestCase
from spacetrading.create_svg import generate_gameboard, generate_planet_market
from spacetrading.models import Game
from spacetrading.models import create_game

class GeneratePrintingMaterial(TestCase):
    def setUp(self):
        pass

    def test_generate_empty_gameboard(self):
        create_game("empty_gameboard", 0, None)
        game = Game.objects.get(game_name="empty_gameboard")
        planets = game.planets.all().order_by('number_of_hexes')
        for planet in planets:
            planet.current_position = -1

        svg_string = generate_gameboard.draw_gameboard(
            game,
            planets,
            [],
            False,
            bg_image="../static/auth/bg.jpeg",
            printing_material=True
        )
        svg_filename = "printing_material/gameboard.svg"
        with open(svg_filename, "w") as svg_file:
            svg_file.write(svg_string)
        """
        html_filename = "printing_material/gameboard.html"
        with open(html_filename, "w") as html_file:
            html_file.write("<!DOCTYPE html><body>")
            html_file.write(svg_string)
            html_file.write("</body>")
        """

    def test_generate_empty_panet_markets(self):
        create_game("empty_gameboard", 0, None)
        game = Game.objects.get(game_name="empty_gameboard")
        planets = game.planets.all().order_by('number_of_hexes')
        for planet in planets:
            planet.buy_resources[0] = '0'
            planet.sell_resources[0] = '0'
        svg_string = generate_planet_market.draw_planet_market(planets)
        svg_filename = "printing_material/planet_market.svg"
        with open(svg_filename, "w") as svg_file:
            svg_file.write(svg_string)
        """
        html_filename = "printing_material/planet_market.html"
        with open(html_filename, "w") as html_file:
            html_file.write("<!DOCTYPE html><body>")
            html_file.write(svg_string)
            html_file.write("</body>")
        """
