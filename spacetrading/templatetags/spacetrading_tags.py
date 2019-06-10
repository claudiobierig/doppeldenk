from django import template
from spacetrading.logic import move

register = template.Library()


@register.simple_tag
def get_class(label):
    if "Buy" in label:
        return "table-danger"
    elif "Sell" in label:
        return "table-success"
    else:
        return "table-light"

@register.simple_tag
def is_active(player, players):
    active_player = move.get_active_player(players)
    return player is active_player
