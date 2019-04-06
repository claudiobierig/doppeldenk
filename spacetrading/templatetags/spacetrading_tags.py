from django import template
import math

register = template.Library()

@register.simple_tag
def is_active(player, players):
    for other_player in players:
        if other_player.time_spent < player.time_spent or other_player.time_spent == player.time_spent and other_player.last_move > player.last_move:
            return False

    return True

@register.simple_tag
def can_trade_resource(resource, resources):
    if resource in resources:
        return True
    return False


@register.simple_tag
def get_cost_resource(resource, resources, cost_resources):
    for res, cost in zip(resources, cost_resources):
        if res == resource:
            return str(cost)
    return ""


@register.filter
def at(l, i):
    try:
        return l[i]
    except:
        return None
