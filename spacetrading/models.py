from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

from spacetrading.logic import move, gamesettings

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

    def get_json(self):
        planet_data = {
            'name': self.name,
            'colour': self.colour,
            'number_of_hexes': self.number_of_hexes,
            'position_of_hexes': self.position_of_hexes,
            'current_position': self.current_position,
            'buy_resources': self.buy_resources,
            'cost_buy_resource': self.cost_buy_resource,
            'sell_resources': self.sell_resources,
            'cost_sell_resource': self.cost_sell_resource,
            'radius_x': self.radius_x,
            'radius_y': self.radius_y,
            'offset': self.offset
        }
        return planet_data

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
            player_number=0,
            has_passed=False
    ):
        if ship_position is None:
            ship_position = [0, 0]
        if resources is None:
            resources = [0, 0, 0, 0, 0]
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
            player_number=player_number,
            has_passed=has_passed
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
        models.IntegerField(),
        5
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
    has_passed = models.BooleanField(default=False)

    objects = PlayerManager()

    def get_json(self):
        player_data = {
            #'name': self.user.get_username(),
            'resources': self.resources,
            'money': self.money,
            'ship_position': self.ship_position,
            'last_move': self.last_move,
            'time_spent': self.time_spent,
            'colour': self.colour,
            'ship_offset': self.ship_offset,
            'player_number': self.player_number,
            'has_passed': self.has_passed
        }
        return player_data

    def __str__(self):
        return f"User {self.user}"


class GameManager(models.Manager):
    def create_game(
            self,
            game_name="",
            number_of_players=1,
            next_move_number=0,
            game_state='w',
            planet_rotation_event_time=gamesettings.PLANET_ROTATION_TIME,
            planet_rotation_event_move=0,
            offer_demand_event_time=gamesettings.OFFER_DEMAND_EVENT_TIMES[0],
            offer_demand_event_move=0,
            planet_influence_track=None,
            resource_limit=9
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
            offer_demand_event_time=offer_demand_event_time,
            offer_demand_event_move=offer_demand_event_move,
            planet_influence_track=planet_influence_track,
            resource_limit=resource_limit
        )
        return game

    def next(self, user, current_id=0):
        all_games = self.filter(players__user=user).filter(
            game_state='r').order_by('id')
        game_gt = all_games.filter(id__gt=current_id)
        for game in game_gt:
            if user == game.get_active_user():
                return game

        game_lt = all_games.filter(id__lt=current_id)
        for game in game_lt:
            if user == game.get_active_user():
                return game

        return False


class Game(models.Model):
    """
    Space Trading Model
    """
    game_name = models.CharField(max_length=100, blank=True, null=True)
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

    offer_demand_event_time = models.IntegerField()
    offer_demand_event_move = models.IntegerField()

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

    resource_limit = models.IntegerField(default=9)

    objects = GameManager()

    def get_absolute_url(self):
        """Returns the url to access a game."""
        return reverse('game_detail', args=[str(self.id)])

    def is_active(self):
        """Return True if game_state is running otherwise False"""
        return (self.game_state is 'r')

    def get_users(self):
        user_group_set = set()
        for player in self.players.all():
            user_group_set.add(player.user)

        return user_group_set

    def get_active_player(self):
        return move.get_active_player(self.players.all())

    def get_active_user(self):
        return self.get_active_player().user

    def get_json(self, players=None, planets=None):
        if players is None:
            players = self.players.all().order_by('player_number')
        if planets is None:
            planets = self.planets.all().order_by('number_of_hexes')

        game_data = {
            'players': [player.get_json() for player in players],
            'planets': [planet.get_json() for planet in planets],
            'game_name': self.game_name,
            'number_of_players': self.number_of_players,
            'next_move_number': self.next_move_number,
            'planet_rotation_event_time': self.planet_rotation_event_time,
            'planet_rotation_event_move': self.planet_rotation_event_move,
            'offer_demand_event_time': self.offer_demand_event_time,
            'offer_demand_event_move': self.offer_demand_event_move,
            'resource_limit': self.resource_limit,
            'game_state': self.game_state,
            'planet_influence_track': self.planet_influence_track
        }

        return game_data

    def __str__(self):
        """String for representing the Model object."""
        return str(
            "id={game.id}, "
            "game_name={game.game_name}, "
            "number_of_players={game.number_of_players}, "
            "next_move_number={game.next_move_number}, "
            "game_state={game.game_state}".format(game=self)
        )
