from django import template
import math

register = template.Library()

@register.simple_tag
def get_colour(planets, coord_q, coord_r):
    for planet in planets:
        if is_from_planet(planet, coord_q, coord_r) is not -1:
            return planet.colour

    return "white"

def is_from_planet(planet, coord_q, coord_r):
    for index, coords in enumerate(planet.position_of_hexes):
        if coords[0] == coord_q and coords[1] == coord_r:
            return index
    
    return -1

@register.simple_tag
def get_opacity(planets, coord_q, coord_r):
    for planet in planets:
        index = is_from_planet(planet, coord_q, coord_r)
        if index is not -1:
            if index is planet.current_position:
                return "1"
            else:
                return "0.3"
    
    return "0"


@register.simple_tag
def print_coordinates(planets, coord_q, coord_r):
    for planet in planets:
        if is_from_planet(planet, coord_q, coord_r) is not -1:
            return True
    return False

@register.simple_tag
def z_coord(coordinates):
    return -coordinates[0]-coordinates[1]

def get_hex_center(coordinates, hex_size, width, height):
    """
    convert hex coordinates to position (center of hex)
    """
    (coord_q, coord_r) = coordinates
    position_x = hex_size * 3. / 2 * coord_q
    position_y = hex_size * \
        (math.sqrt(3) / 2 * coord_q + math.sqrt(3) * coord_r)
    return [position_x + width / 2, position_y + height / 2]

@register.simple_tag
def get_x_position_text(coordinates, hex_size, width, height):
    hex_center = get_hex_center(coordinates, hex_size, width, height)
    return hex_center[0]


@register.simple_tag
def get_y_position_text(coordinates, hex_size, width, height, y_offset):
    hex_center = get_hex_center(coordinates, hex_size, width, height)
    return hex_center[1] - hex_size / 2 - y_offset

@register.filter
def at(l, i):
    try:
        return l[i]
    except:
        return None
