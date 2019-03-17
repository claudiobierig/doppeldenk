from django import template
import math

register = template.Library()

@register.simple_tag
def is_active(player, players):
    for other_player in players:
        if other_player.time_spent < player.time_spent or other_player.time_spent == player.time_spent and other_player.last_move > player.last_move:
            return False

    return True

@register.filter
def at(l, i):
    try:
        return l[i]
    except:
        return None
