from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

from spacetrading.logic import move

import random

# Create your models here.

RESOURCES = (
    ('0', 'no resource'),
    ('1', 'resource1'),
    ('2', 'resource2'),
    ('3', 'resource3'),
    ('4', 'resource4'),
    ('5', 'resource5'),
)


class PlanetManager(models.Manager):
    def create_planet(
            self,
            colour="#000000",
            name="",
            number_of_hexes=1,
            current_position=0,
            radius_x=100,
            radius_y=100,
            offset=0,
            buy_resources=None,
            cost_buy_resource=None,
            sell_resources=None,
            cost_sell_resource=None,
            position_of_hexes=None,
    ):
        if buy_resources is None:
            buy_resources = ['0', '0', '0', '0', '0']
        if cost_buy_resource is None:
            cost_buy_resource = [0, 0, 0, 0, 0]
        if sell_resources is None:
            sell_resources = ['0', '0', '0', '0', '0']
        if cost_sell_resource is None:
            cost_sell_resource = [0, 0, 0, 0, 0]
        if position_of_hexes is None:
            position_of_hexes = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                               [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        
        planet = self.create(
            name=name,
            colour=colour,
            number_of_hexes=number_of_hexes,
            current_position=current_position,
            buy_resources=buy_resources,
            cost_buy_resource=cost_buy_resource,
            sell_resources=sell_resources,
            cost_sell_resource=cost_sell_resource,
            position_of_hexes=position_of_hexes,
            radius_x=radius_x,
            radius_y=radius_y,
            offset=offset
        )
        return planet


class Planet(models.Model):
    """
        - name (string)
        - colour (string)
        - number_of_hexes (int)
        - current_position (int)
        - buy_resources[5] (enum)
        - cost_buy_resource[5] (int)
        - sell_resources[5] (enum)
        - cost_sell_resource[5] (int)
    """
    name = models.CharField(max_length=50)
    colour = models.CharField(max_length=50, default="#000000")
    number_of_hexes = models.IntegerField()
    position_of_hexes = ArrayField(
        ArrayField(
            models.IntegerField(default=0),
            2
        ),
        20
    )
    current_position = models.IntegerField()
    buy_resources = ArrayField(
        models.CharField(
            max_length=1,
            choices=RESOURCES,
            blank=True,
            default='0',
            help_text='Kind of Resource to buy',
        ),
        5
    )
    cost_buy_resource = ArrayField(
        models.IntegerField(),
        5
    )
    sell_resources = ArrayField(
        models.CharField(
            max_length=1,
            choices=RESOURCES,
            blank=True,
            default='0',
            help_text='Kind of Resource for sell',
        ),
        5
    )
    cost_sell_resource = ArrayField(
        models.IntegerField(),
        5
    )

    radius_x = models.IntegerField()
    radius_y = models.IntegerField()
    offset = models.FloatField()

    objects = PlanetManager()


    def __str__(self):
        return str("name: {planet.name}, "
                    "number_of_hexes: {planet.number_of_hexes}, "
                    "current_position: {planet.current_position}, "
                    "buy_resources: {planet.buy_resources}, "
                    "cost_buy_resource: {planet.cost_buy_resource}, "
                    "sell_resources: {planet.sell_resources}, "
                    "cost_sell_resource: {planet.cost_sell_resource}".format(planet=self))

class PlayerManager(models.Manager):
    def create_player(
            self,
            user=None,
            resources=None,
            money=10,
            last_move=-1,
            time_spent=-1,
            ship_position=None,
            colour="white",
            ship_offset=None,
            player_number=0
    ):
        if ship_position is None:
            ship_position = [2, 2]
        if resources is None:
            resources = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        if ship_offset is None:
            ship_offset = [0, 0]
        player = self.create(
            user=user,
            resources=resources,
            money=money,
            last_move=last_move,
            time_spent=time_spent,
            ship_position=ship_position,
            colour=colour,
            ship_offset=ship_offset,
            player_number=player_number
        )
        return player

class Player(models.Model):
    """
        - user (user)
        - resources[9] (enum)
        - money (int)
        - ship_position (int, int)
        - last move (int)
        -
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    resources = ArrayField(
        models.CharField(
            max_length=1,
            choices=RESOURCES,
            blank=True,
            default='0',
            help_text='Cargo of the player',
        ),
        9
    )
    money = models.IntegerField()
    ship_position = ArrayField(
        models.IntegerField(),
        2
    )
    last_move = models.IntegerField()
    time_spent = models.IntegerField()
    colour = models.CharField(max_length=100)
    ship_offset = ArrayField(
        models.IntegerField(),
        2
    )
    player_number = models.IntegerField()

    objects = PlayerManager()

    def __str__(self):
        return f"User {self.user}"


class GameManager(models.Manager):
    def create_game(
            self,
            game_name="",
            number_of_players=1,
            next_move_number=0,
            game_state='w',
            planet_rotation_event_time=10,
            planet_rotation_event_move=0,
            offer_demand_time_event_time=20,
            offer_demand_time_event_move=0,
            planet_influence_track=None
    ):
        if planet_influence_track is None:
            planet_influence_track = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        game = self.create(
            game_name=game_name,
            number_of_players=number_of_players,
            next_move_number=next_move_number,
            game_state=game_state,
            planet_rotation_event_time=planet_rotation_event_time,
            planet_rotation_event_move=planet_rotation_event_move,
            offer_demand_time_event_time=offer_demand_time_event_time,
            offer_demand_time_event_move=offer_demand_time_event_move,
            planet_influence_track=planet_influence_track
        )
        return game

class Game(models.Model):
    """
    Space Trading Model
    """
    game_name = models.CharField(max_length=100)
    number_of_players = models.IntegerField()
    next_move_number = models.IntegerField()
    players = models.ManyToManyField(Player)
    planets = models.ManyToManyField(Planet)

    GAME_STATE = (
        ('w', 'waiting'),
        ('r', 'running'),
        ('f', 'finished')
    )

    planet_rotation_event_time = models.IntegerField()
    planet_rotation_event_move = models.IntegerField()

    offer_demand_time_event_time = models.IntegerField()
    offer_demand_time_event_move = models.IntegerField()

    planet_influence_track = ArrayField(
        ArrayField(
            models.IntegerField(),
            4
        ),
        5
    )

    game_state = models.CharField(
        max_length=1,
        choices=GAME_STATE,
        blank=True,
        default='w',
        help_text='In which state is the game',
    )

    objects = GameManager()

    def get_absolute_url(self):
        """Returns the url to access a game."""
        return reverse('game_detail', args=[str(self.id)])

    def is_active(self):
        """Return True if game_state is running otherwise False"""
        return (self.game_state is 'r')

    def get_users(self):
        user_group_set = set() #self.players.select_related('user')
        for player in self.players.all():
            user_group_set.add(player.user)

        return user_group_set

    def get_active_player(self):
        return move.get_active_player(self.players.all())

    def __str__(self):
        """String for representing the Model object."""
        return str(
            "id={game.id}, "
            "game_name={game.game_name}, "
            "number_of_players={game.number_of_players}, "
            "next_move_number={game.next_move_number}, "
            "game_state={game.game_state}".format(game=self)
        )

def create_game(name, number_of_players, user):
    #TODO: make this error safe and in doubt clean up afterwards
    offer_demand_time_event_times = [40, 30, 25, 20]
    game = Game.objects.create_game(
        game_name=name,
        number_of_players=number_of_players,
        offer_demand_time_event_time=offer_demand_time_event_times[number_of_players-1]
    )
    b_resources = ['1', '2', '3', '4', '5']
    s_resources = ['1', '2', '3', '4', '5']
    random.shuffle(b_resources)
    #TODO: make sure not the same resource at the planet
    random.shuffle(s_resources)
    min_buy_price = 2
    max_buy_price = 4
    min_sell_price = 3
    max_sell_price = 5

    player = Player.objects.create_player(
        user=user,
        colour="#FF0000",
        ship_offset=[0, 0],
        player_number=0
    )
    game.players.add(player)
    planets = [
        [
            "alpha",
            3,
            "#FF0000", 
            [[5, -2], [-3, 4], [-3, -1]],
            [150, 100],
            0
        ],
        [
            "beta",
            5,
            "#FF8000",
            [[7, -3], [1, 3], [-6, 5], [-5, 0], [3, -5]],
            [210, 130],
            0.2
        ],
        [
            "gamma",
            7,
            "#FFFF00",
            [[8, -2], [2, 4], [-5, 7], [-9, 5], [-6, -1], [2, -6], [7, -6]],
            [260, 180],
            0.4
        ],
        [
            "delta",
            11,
            "#008000",
            [[9, -1], [4, 4], [-2, 7], [-7, 8], [-10, 7], [-10, 3], [-7, -1], [-1, -6], [5, -8], [9, -8], [11, -5]],
            [320, 210],
            0.6
        ],
        [
            "epsilon",
            13,
            "#1E90FF",
            [[8, 1], [3, 5], [-2, 8], [-8, 9], [-11, 8], [-12, 5], [-11, 2], [-6, -3], [0, -7], [5, -9], [10, -9], [12, -7], [12, -4]],
            [370, 240],
            0.8
        ]
    ]
    
    for index, pl in enumerate(planets):
        planet = Planet.objects.create_planet(
            name=pl[0],
            colour=pl[2],
            number_of_hexes=pl[1],
            current_position=random.randint(0, pl[1] - 1),
            buy_resources=[b_resources[index], '0', '0', '0', '0'],
            cost_buy_resource=[random.randint(min_buy_price, max_buy_price), 0, 0, 0, 0],
            sell_resources=[s_resources[index], '0', '0', '0', '0'],
            cost_sell_resource=[random.randint(min_sell_price, max_sell_price), 0, 0, 0, 0],
            position_of_hexes=pl[3],
            radius_x=pl[4][0],
            radius_y=pl[4][1],
            offset=pl[5]
        )
        game.planets.add(planet)
    
    if number_of_players == 1:
        game.game_state = 'r'
    game.save()
    player.save()

def join_game(primary_key_game, user):
    game = Game.objects.get(pk=primary_key_game)
    number_of_joined_players = game.players.count()
    if number_of_joined_players >= game.number_of_players or number_of_joined_players > 3:
        return

    colours = ["#FF0000", "#0000FF", "#FFFFFF", "#00FF00"]
    offsets = [[0, 0], [-10, 0], [-10, -15], [0, -15]]
    player = Player.objects.create_player(
        user=user,
        colour=colours[number_of_joined_players],
        ship_offset=offsets[number_of_joined_players],
        player_number=number_of_joined_players
    )
    game.players.add(player)

    if number_of_joined_players >= game.number_of_players - 1:
        #TODO: error handling for > case
        players = game.players.all()
        player_numbers = list(range(len(players)))
        random.shuffle(player_numbers)
        for index, current_player in enumerate(players):
            current_player.player_number = player_numbers[index] + 1
            current_player.last_move = -current_player.player_number
            current_player.save()
        game.game_state = 'r'

    game.save()
