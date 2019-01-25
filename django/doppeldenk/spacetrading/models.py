from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

RESOURCES = (
    ('0', 'no resource'),
    ('1', 'resource1'),
    ('2', 'resource2'),
    ('3', 'resource3'),
    ('4', 'resource4'),
    ('5', 'resource5'),
)


class Planet(models.Model):
    """
        - name (string)
        - number_of_hexes (int)
        - current_position (int)
        - buy_resources[5] (enum)
        - buy_resources_price[5] (int)
        - sell_resources[5] (enum)
        - sell_resources_price[5] (int)
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


    def __str__(self):
        return str(self.name)

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


    def __str__(self):
        return f"User {self.user}"


class Game(models.Model):
    """
    Space Trading Model
    """
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


    def __str__(self):
        """String for representing the Model object."""
        return str(self.id)
