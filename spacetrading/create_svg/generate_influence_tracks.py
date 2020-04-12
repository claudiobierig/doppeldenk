#!/usr/bin/env python
"""
generate influence tracks
"""
from spacetrading.create_svg.svg_commands import Svg
from spacetrading.create_svg import generate_svg_symbols

SIZE_TIMEBOX = 30
HEIGHT = 21 * SIZE_TIMEBOX


def draw_influence_tracks(game, planets, players):
    """
    draw the influence tracks including the markers of the players
    """
    planet_tracks_svg = Svg(
        width=str(len(planets)*SIZE_TIMEBOX),
        height=str(HEIGHT),
        id_name="planet_influence_tracks"
    )
    generate_svg_symbols.add_posibility_for_disc_3d(planet_tracks_svg)
    for planet in planets:
        planet_number = planet.planet_number
        for field in range(0, 21):
            x_pos = planet_number*SIZE_TIMEBOX
            y_pos = HEIGHT - (field + 1)*SIZE_TIMEBOX
            planet_tracks_svg.create_rectangle(
                [x_pos, y_pos],
                [SIZE_TIMEBOX, SIZE_TIMEBOX],
                "{}_influence_{}".format(planet.name, field),
                fill_colour=planet.colour,
                stroke_colour="black"
            )
            if field % 10 == 0:
                planet_tracks_svg.create_rectangle(
                    [x_pos, y_pos],
                    [SIZE_TIMEBOX, SIZE_TIMEBOX],
                    "{}_influence_{}_transperent".format(planet.name, field),
                    fill_colour="black",
                    fill_opacity="0.4"
                )
            planet_tracks_svg.create_text(
                "{}_influence_{}_text".format(planet.name, field),
                (x_pos + SIZE_TIMEBOX / 2, y_pos + SIZE_TIMEBOX / 2 + 4),
                str(field),
                font_size=8
            )
        planet_points = []
        for player in players:
            points = game.planet_influence_track[planet_number][player.player_number]
            # TODO: points larger than 20
            stack_position = planet_points.count(points)
            planet_points.append(points)
            x_pos = planet_number*SIZE_TIMEBOX
            y_pos = (20 - points)*SIZE_TIMEBOX + 15 - 4*stack_position
            planet_tracks_svg.use_symbol(
                'disc_3d',
                'influence_marker_{}_{}'.format(player.player_number, planet.name),
                position=[x_pos, y_pos],
                fill_colour=player.colour
            )
    svg_string = planet_tracks_svg.get_string()
    return svg_string


if __name__ == '__main__':
    pass
