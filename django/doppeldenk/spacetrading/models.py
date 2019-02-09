from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

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
            self, name="", number_of_hexes=1, current_position=0,
            buy_resources=['0', '0', '0', '0', '0'],
            cost_buy_resource=[0, 0, 0, 0, 0],
            sell_resources=['0', '0', '0', '0', '0'],
            cost_sell_resource=[0, 0, 0, 0, 0]
    ):
        planet = self.create(name=name, number_of_hexes=number_of_hexes, current_position=current_position,
            buy_resources=buy_resources,
            cost_buy_resource=cost_buy_resource,
            sell_resources=sell_resources,
            cost_sell_resource=cost_sell_resource)
        return planet


class Planet(models.Model):
    """
        - name (string)
        - number_of_hexes (int)
        - current_position (int)
        - buy_resources[5] (enum)
        - cost_buy_resource[5] (int)
        - sell_resources[5] (enum)
        - cost_sell_resource[5] (int)
    """
    name = models.CharField(max_length=50)
    number_of_hexes = models.IntegerField()
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
            time_spent=0
    ):
        if resources is None:
            resources = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        player = self.create(
            user=user,
            resources=resources,
            money=money,
            last_move=last_move,
            time_spent=time_spent
        )
        return player

class Player(models.Model):
    """
        - user (user)
        - resources[9] (enum)
        - money (int)
        - ship_position (planet)
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
    ship_position = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, blank=True)
    last_move = models.IntegerField()
    time_spent = models.IntegerField()

    objects = PlayerManager()

    def __str__(self):
        return f"User {self.user}"


class GameManager(models.Manager):
    def create_game(
            self,
            game_name="",
            number_of_players=1,
            next_move_number=-1,
            next_move_type='f',
            game_state='w'
    ):
        game = self.create(
            game_name=game_name,
            number_of_players=number_of_players,
            next_move_number=next_move_number,
            next_move_type=next_move_type,
            game_state=game_state
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

    MOVE_TYPE = (
        ('m', 'Market action'),
        ('f', 'Fly to another planet')
    )

    next_move_type = models.CharField(
        max_length=1,
        choices=MOVE_TYPE,
        blank=True,
        default='f',
        help_text='What is the next move type',
    )

    GAME_STATE = (
        ('w', 'waiting'),
        ('r', 'running'),
        ('f', 'finished')
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

    def __str__(self):
        """String for representing the Model object."""
        return str(
            "id={game.id}, "
            "game_name={game.game_name}, "
            "number_of_players={game.number_of_players}, "
            "next_move_number={game.next_move_number}, "
            "next_move_type={game.next_move_type}, "
            "game_state={game.game_state}".format(game=self)
        )

def create_game(name, number_of_players, user):
    #TODO: make this error safe and in doubt clean up afterwards
    game = Game.objects.create_game()
    game.game_name = name
    game.number_of_players = number_of_players
    b_resources = ['1', '2', '3', '4', '5']
    s_resources = ['1', '2', '3', '4', '5']
    random.shuffle(b_resources)
    #TODO: make sure not the same resource at the planet
    random.shuffle(s_resources)
    min_buy_price = 2
    max_buy_price = 4
    min_sell_price = 3
    max_sell_price = 5

    player = Player.objects.create_player(user=user)
    game.players.add(player)
    planets = [["alpha", 3], ["beta", 5], ["gamma", 7], ["delta", 11], ["epsilon", 13]]
    starting_position = random.randint(0, 5)
    for index, pl in enumerate(planets):
        planet = Planet.objects.create_planet(
            name=pl[0],
            number_of_hexes=pl[1],
            current_position=random.randint(0, pl[1] - 1),
            buy_resources=[b_resources[index], '0', '0', '0', '0'],
            cost_buy_resource=[random.randint(min_buy_price, max_buy_price), 0, 0, 0, 0],
            sell_resources=[s_resources[index], '0', '0', '0', '0'],
            cost_sell_resource=[random.randint(min_sell_price, max_sell_price), 0, 0, 0, 0]
        )
        game.planets.add(planet)
        if index is starting_position:
            player.ship_position_id = planet.id
    
    if number_of_players == 1:
        game.game_state = 'r'
    game.save()
    player.save()

def join_game(primary_key_game, user):
    game = Game.objects.get(pk=primary_key_game)
    player = Player.objects.create_player(user=user)
    game.players.add(player)
    number_of_joined_players = game.players.count()
    if number_of_joined_players >= game.number_of_players:
        #TODO: error handling for > case
        game.game_state = 'r'

    game.save()
