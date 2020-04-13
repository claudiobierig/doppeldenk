from django.test import TestCase
from spacetrading.create_svg import generate_gameboard
from spacetrading.create_svg import generate_planet_market
from spacetrading.create_svg import generate_printing_player_boards
from spacetrading.create_svg import generate_plain_symbols
from spacetrading.create_svg import generate_svg_symbols
from spacetrading.create_svg.svg_commands import Svg
from spacetrading.models import Game
from spacetrading.logic.initialize import create_game


def generate_symbol_svg(name, scaling=None):
    svg = Svg(width=30, height=30, id_name="{}_svg".format(name))
    generate_svg_symbols.add_posibility_for_symbol(svg, name)
    additional_arguments = {}
    if scaling is not None:
        additional_arguments["transform"] = "scale({})".format(scaling)
    svg.use_symbol(name, "{}_id".format(name), position=[
                   0, 0], additional_arguments=additional_arguments)
    return svg


class GeneratePrintingMaterial(TestCase):
    def setUp(self):
        pass

    def test_generate_empty_gameboard(self):
        data = {
            "name": "empty_gameboard",
            "number_of_players": 0,
            "play_all_players": False,
            "resource_limit": 5
        }
        create_game(
            data,
            None
        )
        game = Game.objects.get(game_name="empty_gameboard")
        planets = game.planets.all().order_by('planet_number')
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
        data = {
            "name": "empty_gameboard",
            "number_of_players": 0,
            "play_all_players": False,
            "resource_limit": 5
        }
        create_game(
            data,
            None
        )
        game = Game.objects.get(game_name="empty_gameboard")
        planets = game.planets.all().order_by('planet_number')
        for planet in planets:
            planet.planet_demand_resources[0] = '0'
            planet.planet_supply_resources[0] = '0'
        svg_strings = [str(svg) for svg in generate_planet_market.draw_planet_market(planets)]
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
        data = {
            "name": "empty_gameboard",
            "number_of_players": 0,
            "play_all_players": False,
            "resource_limit": 5
        }
        create_game(
            data,
            None
        )
        game = Game.objects.get(game_name="empty_gameboard")
        players = game.players.all()
        svg_string = generate_printing_player_boards.draw_player_boards(
            players)
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

        planet_rotation_svg = generate_symbol_svg("planet_rotation")
        production_svg = generate_symbol_svg("production")
        time_svg = generate_symbol_svg("time", scaling=1.5)
        politician_svg = generate_symbol_svg("politician")
        influence_svg = generate_symbol_svg("influence", scaling=1.5)
        star_svg = generate_symbol_svg("star")
        planet_svg = generate_symbol_svg("planet")

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
            html_file.write(time_svg.get_string())
            html_file.write(politician_svg.get_string())
            html_file.write(influence_svg.get_string())
            html_file.write(star_svg.get_string())
            html_file.write(planet_svg.get_string())

            html_file.write("</body>")
