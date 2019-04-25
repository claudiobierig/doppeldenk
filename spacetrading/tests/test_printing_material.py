from django.test import TestCase
from spacetrading.create_svg import generate_gameboard, generate_planet_market, generate_printing_player_boards, generate_plain_symbols, generate_svg_symbols
from spacetrading.create_svg.svg_commands import Svg
from spacetrading.models import Game
from spacetrading.models import create_game

class GeneratePrintingMaterial(TestCase):
    def setUp(self):
        pass

    def test_generate_empty_gameboard(self):
        create_game("empty_gameboard", 0, False, None)
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

    def test_generate_empty_planet_markets(self):
        create_game("empty_gameboard", 0, False, None)
        game = Game.objects.get(game_name="empty_gameboard")
        planets = game.planets.all().order_by('number_of_hexes')
        for planet in planets:
            planet.buy_resources[0] = '0'
            planet.sell_resources[0] = '0'
        svg_strings = generate_planet_market.draw_planet_market(game, planets, [])
        svg_filename = "printing_material/planet_market_{}.svg"
        for index in range(len(planets)):
            with open(svg_filename.format(index), "w") as svg_file:
                svg_file.write(svg_strings[index])
        html_filename = "printing_material/planet_market.html"
        with open(html_filename, "w") as html_file:
            html_file.write("<!DOCTYPE html><body>")
            html_file.write(svg_strings[0])
            html_file.write("<br>")
            html_file.write(svg_strings[1])
            html_file.write("<br>")
            html_file.write(svg_strings[2])
            html_file.write("<br>")
            html_file.write(svg_strings[3])
            html_file.write("<br>")
            html_file.write(svg_strings[4])
            html_file.write("</body>")

    def test_generate_empty_playerboards(self):
        create_game("empty_gameboard", 4, True, None)
        game = Game.objects.get(game_name="empty_gameboard")
        players = game.players.all()
        svg_string = generate_printing_player_boards.draw_player_boards(players)
        svg_filename = "printing_material/player_boards.svg"
        with open(svg_filename, "w") as svg_file:
            svg_file.write(svg_string)
        html_filename = "printing_material/player_boards.html"
        with open(html_filename, "w") as html_file:
            html_file.write("<!DOCTYPE html><body>")
            html_file.write(svg_string)
            html_file.write("</body>")
    
    def test_generate_symbols(self):
        svgs = generate_plain_symbols.draw_symbols()
        planet_rotation_svg = Svg(width=30, height=30, id_name="planet_rotation_svg")
        generate_svg_symbols.add_posibility_for_planet_rotation(planet_rotation_svg)
        planet_rotation_svg.use_symbol("planet_rotation", "planet_rotation_id", position=[0, 0])
        production_svg = Svg(width=30, height=30, id_name="production_svg")
        generate_svg_symbols.add_posibility_for_production(production_svg)
        production_svg.use_symbol("production", "production_id", position=[0, 0])

        html_filename = "printing_material/symbols.html"
        with open(html_filename, "w") as html_file:
            html_file.write("<!DOCTYPE html><body>")
            for _ in range(4):
                html_file.write(svgs["red_cross"])
                html_file.write(svgs["radioactive"])
                html_file.write(svgs["food"])
                html_file.write(svgs["water"])
                html_file.write(svgs["building_resource"])
                html_file.write("<br>")
            html_file.write(planet_rotation_svg.get_string())
            html_file.write(planet_rotation_svg.get_string())
            html_file.write(planet_rotation_svg.get_string())
            html_file.write(production_svg.get_string())
            html_file.write(production_svg.get_string())
            html_file.write("<br>")

            html_file.write("</body>")

