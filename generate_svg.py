#!/usr/bin/env python

import lxml
from lxml import etree
from lxml import html
import math


# TODO: make this options
hex_size = 20
font_size = 6

padding = 100
font_padding = 5
filename = "index.html"

ship_width = 10
ship_height = 20


class Planet:
    def __init__(self,(radius_x,radius_y),col, number_hexes, planet_name):
        self.rx = radius_x
        self.ry = radius_y
        self.colour = col
        self.number_of_hexes = number_hexes
        self.name = planet_name

class Player:
    def __init__(self,player_name,col):
        self.name = player_name
        self.colour = col

planets = [
            Planet((150,100),'#FF0000',3,'alpha'),
            Planet((210,130),'#FF8000',5,'beta'),
            Planet((260,180),'#FFFF00',7,'gamma'),
            Planet((320,210),'#008000',11,'delta'),
            Planet((370,240),'#1E90FF',13,'epsilon')
          ]

players = [
            Player("player1", "#FF0000"),
            Player("player2", "#0000FF"),
            Player("player3", "#FFFFFF"),
            Player("player4", "#00FF00")
          ]

width = 2*(planets[-1].rx + padding)
height = 2*(planets[-1].ry + padding)


def get_hex_coordinates((x,y), hex_size):
    q = ( 2./3 * x ) / hex_size
    r = (-1./3 * x + math.sqrt(3)/3 * y) / hex_size
    return [round(q),round(r)]

def get_hex_center((q,r), hex_size):
    x = hex_size * 3./2 * q
    y = hex_size * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
    return [x, y]

def jsonToStyle(json):
    style_argument = ""
    for attribute,value in json.items():
        style_argument = style_argument + attribute + ":" + value + ";"

    return style_argument



def draw_planet(svg, planet, (cx, cy)):
    """
    0. generate layer in here instead of parent
    1. draw ellipse
    2. compute length of elipse
    3. compute where hexes should be
    4. draw hexes and coordinates
    """

    layer = etree.SubElement(svg, 'g', {'id': planet.name, 'class': 'planet'})
    
    svg_ellipse((planet.rx,planet.ry), (cx,cy), planet.colour, layer, planet.name + "_ellipse")

    #compute degree where the hexes should be
    degrees = range(0,planet.number_of_hexes)
    degrees[:] = [x * 2 * math.pi / planet.number_of_hexes for x in degrees]
    positions = [(planet.rx*math.cos(x) + cx,planet.ry*math.sin(x) + cy) for x in degrees]
    print_hexes(positions, planet.colour, layer, planet.name)


def svg_ellipse((rx, ry), (cx, cy), colour, parent, id, fill="none",
                stroke_width="1", stroke_opacity="0.5", opacity="1"):
    """
    <ellipse xmlns="http://www.w3.org/2000/svg" 
    style="opacity:0.53500001;fill:none;fill-rule:evenodd;stroke:#008000;
           stroke-width:10.64384651;stroke-linecap:butt;stroke-linejoin:miter;
           stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" 
           id="path30104" cx="697.71796" cy="-58.367298" rx="521.46375" ry="701.46375"/>
    """
    style = {   'stroke'        : colour,
                'stroke-width'  : stroke_width,
                'stroke-opacity': stroke_opacity,
                #'fill'          : fill,
                #'opacity'       : opacity
            }
    if fill:
        style['fill'] = fill
        style['opacity'] = opacity

    ell_attribs = {
        'style'     : jsonToStyle(style),
        'cx'        : str(cx),
        'cy'        : str(cy),
        'rx'        : str(rx),
        'ry'        : str(ry),
        'id'        : str(id)
        }
    
    etree.SubElement(parent, 'ellipse', ell_attribs )

def svg_hex(id, (cx, cy), colour, parent, parentname, fill_opacity="0.5"):
    #<polygon points="200,10 250,190 160,210" style="fill:lime;stroke:purple;stroke-width:1" />
    hex_width = float(2*hex_size)
    hex_height = math.sqrt(3)*hex_size
    
    points = [
                [cx - hex_width/4, cy - hex_height/2],
                [cx + hex_width/4, cy - hex_height/2],
                [cx + hex_width/2, cy],
                [cx + hex_width/4, cy + hex_height/2],
                [cx - hex_width/4, cy + hex_height/2],
                [cx - hex_width/2, cy]
             ]
    str_points = ""
    for point in points:
        str_points = str_points + str(point[0]) + "," + str(point[1]) + " "

    [q,r]=get_hex_coordinates((cx,cy), hex_size)
    style = {   'stroke'        : '#FFFFFF',
                'stroke-width'  : '1',
                'fill'          : colour,
                'fill-opacity'  : fill_opacity
            }
    ell_attribs = {
        'style'  :jsonToStyle(style),
        'points' :str_points,
        'id'     :parentname + "_" + str(id),
        'coord_q':str(q),
        'coord_r':str(r),
        'onclick':'clickHex(this)',
        'onmouseover': 'mouseOverHex(this)',
        'onmouseout' : 'mouseOutHex(this)',
        'class'  :parentname + "_hex"
            }
    
    etree.SubElement(parent, 'polygon', ell_attribs )
    
def print_hexes(positions, colour, parent, parentname):
    for index, position in enumerate(positions):
        hex_coordinates = get_hex_coordinates(position, hex_size)
        hex_center = get_hex_center(hex_coordinates, hex_size)
        svg_hex(index,hex_center,colour,parent,parentname)
        x = hex_center[0]
        y = hex_center[1] - hex_size/2 - font_size - font_padding
        content = str(int(hex_coordinates[0])) + "," + str(int(hex_coordinates[1])) + "," + str(int(- hex_coordinates[0] - hex_coordinates[1]))
        svg_text((x,y), content, parent, colour="#FFFFFF")

def svg_text((x,y), content, parent, size=font_size, colour="#000000"):
    text = etree.Element('text')
    text.set('x', str(x))
    text.set('y', str(y+font_size/2))
    text.set('style', "text-align:center;text-anchor:middle;font-size:" + str(size) + "pt")
    text.set('fill', colour)
    text.text = content
    text.set('id', content)
    parent.append(text)



def draw_timebox((x,y),(w,h),name,time,parent):
    style = {
        'fill'          : '#AAAAAA',
        'stroke'        : '#000000',
        'stroke-width'  : '1',
        'fill-opacity'  : '1'
    }
    if time % 10 ==0 :
        style['fill'] = "#AAAAAA"
    else:
        style['fill'] = "#FFFFFF"
    etree.SubElement(parent, 'rect', {
                                      'style'   : jsonToStyle(style),
                                      'id'      : name,
                                      'time'    : str(time),
                                      'width'   : str(w),
                                      'height'  : str(h),
                                      'x'       : str(x),
                                      'y'       : str(y),
                                      'class'   : 'timebox',
                                      }
                        )
    svg_text((x+w/2,y+h/2),str(time),parent,8)
    
    events = []
    if time % 20 == 0:
        events.append("planet_rotation")

    draw_events_for_one_timestep((x,y), (w,h), events, time, parent)

def draw_event((cx,cy), r, event, time, parent):
    #TODO: change this when we have different events
    style = {
        'fill'          : '#00FFFF'
    }
    etree.SubElement(parent, 'circle', {
        'style' : jsonToStyle(style),
        'id'    : time + "_" + event,
        'cx'    : str(cx),
        'cy'    : str(cy),
        'r'     : str(r),
        'time'  : time,
        'event' : event,
        'class' : 'event'
        })

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
    layer = etree.SubElement(svg, 'g', {'id': 'timeline'})
    height_timebox = 30
    width_corner = height_timebox
    width_top = (width - 2*width_corner)/29
    width_side = (height - 2*width_corner)/19

    width_timeline = 2*width_corner + 29*width_top
    height_timeline = 2*width_corner + 19*width_side

    draw_timebox((0,0),(width_corner,height_timebox),"timebox_0",0,layer);
    for i in range(1,30):
        draw_timebox((width_corner+(i-1)*width_top,0),(width_top,height_timebox),"timebox_" + str(i), i,layer)

    draw_timebox((width_corner+29*width_top,0),(width_corner,height_timebox),"timebox_30", 30,layer)
    for i in range(31,50):
        draw_timebox((width_corner+29*width_top,width_corner+(i-31)*width_side),(height_timebox,width_side),"timebox_" + str(i), i,layer)

    draw_timebox((width_corner+29*width_top,width_corner+19*width_side),(width_corner,height_timebox),"timebox_50", 50,layer)

    for i in range(51,80):
        draw_timebox((width_corner+(79-i)*width_top,width_corner+19*width_side),(width_top,height_timebox),"timebox_" + str(i), i,layer)

    draw_timebox((0,width_corner+19*width_side),(width_corner,height_timebox),"timebox_80",80,layer);

    for i in range(81,100):
        draw_timebox((0,width_corner+(99-i)*width_side),(height_timebox,width_side),"timebox_" + str(i), i,layer)

    

    return [width_timeline, height_timeline]

def timemarker_symbol(svg):
    symbol = etree.SubElement(svg, 'symbol', {'id': 'timemarker', 'view_box' : '0 0 30 15'})
    svg_ellipse((12, 4), (15, 9), "#000000", symbol, "bottom", False, "1", "1", "1")
    etree.SubElement(symbol, 'rect', {
                                      'id'      : "middle",
                                      'width'   : "24",
                                      'height'  : "4",
                                      'x'       : "3",
                                      'y'       : "5"
                                      }
                        )
    svg_ellipse((12, 4), (15, 5), "#000000", symbol, "top", False, "1", "1", "1")
    linestyle = {
        'stroke'        : '#000000',
        'stroke-width'  : '1',
    }
    etree.SubElement(symbol, 'line', {
                                    'x1': "3",
                                    'x2': "3",
                                    'y1': "5",
                                    'y2': "9",
                                    'style': jsonToStyle(linestyle),
                                   }
        )
    etree.SubElement(symbol, 'line', {
                                    'x1': "27",
                                    'x2': "27",
                                    'y1': "5",
                                    'y2': "9",
                                    'style': jsonToStyle(linestyle),
                                   }
        )

def draw_sun(svg,(width,height),r):
    etree.SubElement(svg,'circle', {'id': 'sun', 'cx': str(width/2), 'cy': str(height/2), 'r': str(r), 'style': 'fill:yellow'})

def draw_ship(parent, player, (x,y)):
    style = {
        'fill' : player.colour
    }
    etree.SubElement(parent, 'rect', {
                                          'style'   : jsonToStyle(style),
                                          'class'   : 'ship',
                                          'id'      : "ship_" + player.name,
                                          'width'   : str(ship_width),
                                          'height'  : str(ship_height),
                                          'x'       : str(x),
                                          'y'       : str(y)
                                          }
                            )

def draw_time_marker(parent, player, (x,y)):
    etree.SubElement(parent, 'use', {'href' : "#timemarker",
                                  'id'   : "timemarker_" + player.name,
                                  'x'    : str(x),
                                  'y'    : str(y),
                                  'time' : "0",
                                  'class': "timemarker",
                                  'style': "fill:" + player.colour})


def draw_players(svg):
    players_group = etree.SubElement(svg, 'g', {'id': 'players'})
    for index, player in enumerate(players):
        player_group = etree.SubElement(players_group, 'g', {'id': player.name})
        draw_time_marker(player_group, player, (0,15-index*4))
        draw_ship(player_group, player, (index*(ship_width+10) + 50,50))

def main():
    svg = etree.Element("svg", {"width" : str(width), "height": str(height), "id": "gameboard"})
    timemarker_symbol(svg)
    etree.SubElement(svg, 'image', {'href' : 'bg.jpeg'})
    [width_timeline, height_timeline] = draw_timeline(svg)
    svg.set('width', str(width_timeline))
    svg.set('height', str(height_timeline))
    for planet in planets:
        draw_planet(svg,planet,(width_timeline/2,height_timeline/2))

    draw_players(svg)
    draw_sun(svg, (width_timeline,height_timeline), hex_size)

    with open("gameboard.svg","w") as f:
        f.write(etree.tostring(svg, pretty_print=True))



if __name__ == '__main__':
    main()
