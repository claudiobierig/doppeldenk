#!/usr/bin/env python

import lxml
from lxml import etree
from lxml import html
import math


# TODO: make this options
hex_size = 20
font_size = 8

padding = 50
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

planets = [
            Planet((200,100),'#FF0000',3,'alpha'),
            Planet((240,130),'#FF00FF',5,'beta'),
            Planet((300,180),'#0000FF',7,'gamma'),
            Planet((340,210),'#FFFF00',11,'delta'),
            Planet((390,230),'#00FF00',13,'epsilon')
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

def draw_ship(svg, (cx, cy), colour, shipname):
    style = {
        'fill' : colour
    }
    ship = etree.SubElement(svg, 'rect', {
                                          'style'   : jsonToStyle(style),
                                          'id'      : shipname,
                                          'width'   : str(ship_width),
                                          'height'  : str(ship_height),
                                          'x'       : str(cx - ship_width/2),
                                          'y'       : str(cy - ship_height/2)
                                          }
                            )

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
                'fill'          : fill,
                'opacity'       : opacity
            }

    ell_attribs = {
        'style'     : jsonToStyle(style),
        'cx'        : str(cx),
        'cy'        : str(cy),
        'rx'        : str(rx),
        'ry'        : str(ry),
        'id'        : str(id)
        }
    
    etree.SubElement(parent, 'ellipse', ell_attribs )

def svg_hex(id, (cx, cy), colour, parent, parentname):
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
    style = {   'stroke'        : '#000000',
                'stroke-width'  : '0.3',
                'fill'          : colour,
                'fill-opacity'  : '0.5'
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
        hex_center = get_hex_center(get_hex_coordinates(position, hex_size), hex_size)
        svg_hex(index,hex_center,colour,parent,parentname)
        svg_text(hex_center,parent)

def svg_text((cx,cy), parent):
    [q,r]=get_hex_coordinates((cx,cy), hex_size)
    """
    style = {   'text-align'        : 'center',
                'text-anchor'       : 'middle',
                'font-size'         : '4pt'
            }
    text_attribs = {
                    'style'     :simplestyle.formatStyle(style),
                    'x'         :cx,
                    'y'         :cy
                    }
    """
    text = etree.Element('text')
    text.set('x', str(cx))
    text.set('y', str(cy - hex_size/2 - font_size - font_padding))
    text.set('style', "text-align:center;text-anchor:middle;font-size:" + str(font_size) + "pt")
    text.text = str(q) + "," + str(r)
    text.set('id', str(q) + "," + str(r))
    parent.append(text)


def main():
    svg = etree.Element("svg", {"width" : str(width), "height": str(height), "id": "gameboard"})
    for planet in planets:
        draw_planet(svg,planet,(width/2,height/2))
    draw_ship(svg,(width/2,height/2),"#AAAAAA","player1")

    with open("gameboard.svg","w") as f:
        f.write(etree.tostring(svg, pretty_print=True))
"""
    #TODO try catch here. Instead generate new svg if html not existened or other than expected
    tree = html.parse(filename)
    gameboard = tree.getroot().get_element_by_id("gameboard")
    parent = gameboard.getparent()
    parent.replace(gameboard,svg)
    
    print(etree.tostring(svg, pretty_print=True))
    #write to file
    with open(filename,"w") as f:
        f.write(etree.tostring(tree, pretty_print=True))
"""
    



if __name__ == '__main__':
    main()
