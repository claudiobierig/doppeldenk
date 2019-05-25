from django import template

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
    for other_player in players:
        if other_player.time_spent < player.time_spent or other_player.time_spent == player.time_spent and other_player.last_move > player.last_move:
            return False

    return True
