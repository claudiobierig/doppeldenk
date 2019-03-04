from spacetrading import models

def move(game, data):
    players = game.players.all()
    active_player = models.get_active_player(players)
    active_player.time_spent = 0
    active_player.last_move = game.next_move_number
    active_player.ship_position = [data['coord_q'], data['coord_r']]
    game.next_move_number = game.next_move_number + 1
    game.save()
    active_player.save()