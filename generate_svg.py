#!/usr/bin/env python


from svg_commands import Svg

from lxml import etree
import math


# TODO: make this options
hex_size = 20
font_size = 6

padding = 100
font_padding = 5
filename = "index.html"

ship_width = 10
ship_height = 20

size_timebox = 30
number_timeboxes_width = 31
number_timeboxes_height = 21
padding_timeboxes = 20

class Planet:
    def __init__(self, (radius_x, radius_y), col, number_hexes, planet_name):
        self.rx = radius_x
        self.ry = radius_y
        self.colour = col
        self.number_of_hexes = number_hexes
        self.name = planet_name

class Player:
    def __init__(self, player_name, col):
        self.name = player_name
        self.colour = col

planets = [
    Planet((150, 100), '#FF0000', 3, 'alpha'),
    Planet((210, 130), '#FF8000', 5, 'beta'),
    Planet((260, 180), '#FFFF00', 7, 'gamma'),
    Planet((320, 210), '#008000', 11, 'delta'),
    Planet((370, 240), '#1E90FF', 13, 'epsilon')
]

players = [
    Player("player1", "#FF0000"),
    Player("player2", "#0000FF"),
    Player("player3", "#FFFFFF"),
    Player("player4", "#00FF00")
]

width = number_timeboxes_width*size_timebox
height = number_timeboxes_height*size_timebox

assert 2*(planets[-1].rx + padding_timeboxes + hex_size + size_timebox) < width
assert 2*(planets[-1].ry + padding_timeboxes + hex_size + size_timebox) < height


def get_hex_coordinates((x, y), hex_size):
    q = (2./3 * x) / hex_size
    r = (-1./3 * x + math.sqrt(3)/3 * y) / hex_size
    return [round(q), round(r)]

def get_hex_center((q, r), hex_size):
    x = hex_size * 3./2 * q
    y = hex_size * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
    return [x, y]

def draw_planet(svg, planet, (cx, cy)):
    """
    0. generate layer in here instead of parent
    1. draw ellipse
    2. compute length of elipse
    3. compute where hexes should be
    4. draw hexes and coordinates
    """
    layer = svg.create_subgroup(planet.name, class_name='planet')
    layer.create_ellipse((planet.rx, planet.ry), 
                         (cx, cy),
                         planet.colour,
                         planet.name + "_ellipse",
                         fill="none")

    #compute degree where the hexes should be
    degrees = range(0, planet.number_of_hexes)
    degrees[:] = [x * 2 * math.pi / planet.number_of_hexes for x in degrees]
    positions = [(planet.rx*math.cos(x) + cx, planet.ry*math.sin(x) + cy) for x in degrees]
    print_hexes(positions, planet.colour, layer, planet.name)

  
def print_hexes(positions, colour, parent, parentname):
    for index, position in enumerate(positions):
        hex_coordinates = get_hex_coordinates(position, hex_size)
        hex_center = get_hex_center(hex_coordinates, hex_size)
        parent.create_hex(parentname + "_" + str(index), hex_center,
                          hex_coordinates, hex_size, colour,
                          parentname + "_hex")
        x = hex_center[0]
        y = hex_center[1] - hex_size/2 - font_size - font_padding
        content = str(int(hex_coordinates[0])) + "," + str(int(hex_coordinates[1])) + "," + str(int(- hex_coordinates[0] - hex_coordinates[1]))
        parent.create_text((x, y), content, font_size=font_size,
                           font_colour="#FFFFFF")



def draw_timebox((x,y),(w,h),name,time,parent):
    fill_colour = "#FFFFFF"
    if time % 10 ==0 :
        fill_colour = "#AAAAAA"
    
    additional_arguments = {
        'time' : str(time),
        'class': 'timebox'
    }

    parent.create_rectangle((x, y), (w, h),
                            name, fill_colour=fill_colour,
                            stroke_colour="#000000",
                            stroke_width=1,
                            fill_opacity=1,
                            additional_arguments=additional_arguments)
    parent.create_text((x+w/2, y+h/2 + 4), str(time),
                       font_size=8)

    events = []
    if time % 20 == 0:
        events.append("planet_rotation")

    draw_events_for_one_timestep((x,y), (w,h), events, time, parent)

def draw_event((cx,cy), r, event, time, parent):
    additional_arguments = {
        'time' : str(time),
        'event' : event,
        'class' : 'event'
    }
    parent.create_circle((cx, cy), r, str(time) + "_" + event,
                         fill_colour='#00FFFF',
                         additional_arguments=additional_arguments)

def draw_events_for_one_timestep((x,y), (w,h), events, time, parent):
    radius = min(w,h)/4

    for index, event in enumerate(events):
        cx=0
        cy=0
        if index ==0:
            cx = x + w/4
            cy = y + h/4
        elif index ==1:
            cx = x + 3*w/4
            cy = y + h/4
        elif index ==2:
            cx = x + w/4
            cy = y + 3*h/4
        elif index ==3:
            cx = x + 3*w/4
            cy = y + 3*h/4
        else:
            print("error: too many events")

        draw_event((cx,cy), radius, event, str(time), parent)


def draw_timeline(svg):
    layer = svg.create_subgroup("timeline")
    for i in range(0, 31):
        draw_timebox((i*size_timebox, 0),
                     (size_timebox, size_timebox),
                     "timebox_" + str(i), i, layer)
    for i in range(31, 51):
        draw_timebox((30*size_timebox, (i-30)*size_timebox),
                     (size_timebox, size_timebox),
                     "timebox_" + str(i), i, layer)
    for i in range(51, 81):
        draw_timebox(((80-i)*size_timebox, 20*size_timebox),
                     (size_timebox, size_timebox),
                     "timebox_" + str(i), i, layer)
    for i in range(81, 100):
        draw_timebox((0, (100-i)*size_timebox),
                     (size_timebox, size_timebox),
                     "timebox_" + str(i), i, layer)

def draw_sun(svg, (width, height), r):
    svg.create_circle((width/2, height/2), r, 'sun', fill_colour='yellow')

def draw_players(svg):
    players_group = svg.create_subgroup('players')
    for index, player in enumerate(players):
        player_group = players_group.create_subgroup(player.name)
        additional_arguments_disc = {
            'time' : '0',
            'class': 'timemarker'
        }
        player_group.create_3d_disc("timemarker_" + player.name,
                                    (0, 15-index*4), fill_colour=player.colour,
                                    additional_arguments=additional_arguments_disc)
        player_group.create_rectangle((index*(ship_width+10) + 50, 50),
                                      (ship_width, ship_height),
                                      "ship_" + player.name,
                                      fill_colour=player.colour,
                                      additional_arguments={'class':'ship'})
        #draw_ship(player_group, player, (index*(ship_width+10) + 50,50))

def main():
    svg = Svg(width=str(width), height=str(height), id_name="gameboard")
    svg.add_posibility_for_disc_3d()
    svg.create_image("bg.jpeg")
    draw_timeline(svg)
    for planet in planets:
        draw_planet(svg, planet, (width/2, height/2))

    draw_sun(svg, (width, height), hex_size)
    draw_players(svg)
    svg_string = svg.get_string()
    print svg_string
    with open("gameboard.svg", "w") as f:
        f.write(svg_string)


if __name__ == '__main__':
    main()
