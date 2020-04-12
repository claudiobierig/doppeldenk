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
            planet_demand_resources=None,
            planet_demand_resources_price=None,
            planet_supply_resources=None,
            planet_supply_resources_price=None,
            position_of_hexes=None,
            planet_number=0,
            add_demand_resource='0',
            add_demand_resource_price=0,
            add_demand_resource_time=0
    ):
        if planet_demand_resources is None:
            planet_demand_resources = ['0', '0', '0', '0', '0']
        if planet_demand_resources_price is None:
            planet_demand_resources_price = [0, 0, 0, 0, 0]
        if planet_supply_resources is None:
            planet_supply_resources = ['0', '0', '0', '0', '0']
        if planet_supply_resources_price is None:
            planet_supply_resources_price = [0, 0, 0, 0, 0]
        if position_of_hexes is None:
            position_of_hexes = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                                 [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

        planet = self.create(
            name=name,
            colour=colour,
            number_of_hexes=number_of_hexes,
            current_position=current_position,
            planet_demand_resources=planet_demand_resources,
            planet_demand_resources_price=planet_demand_resources_price,
            planet_supply_resources=planet_supply_resources,
            planet_supply_resources_price=planet_supply_resources_price,
            position_of_hexes=position_of_hexes,
            radius_x=radius_x,
            radius_y=radius_y,
            offset=offset,
            planet_number=planet_number,
            add_demand_resource=add_demand_resource,
            add_demand_resource_price=add_demand_resource_price,
            add_demand_resource_time=add_demand_resource_time
        )
        return planet


class Planet(models.Model):
    """
        - name (string)
        - colour (string)
        - number_of_hexes (int)
        - current_position (int)
        - planet_demand_resources[5] (enum)
        - planet_demand_resources_price[5] (int)
        - planet_supply_resources[5] (enum)
        - planet_supply_resources_price[5] (int)
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
    planet_demand_resources = ArrayField(
        models.CharField(
            max_length=1,
            choices=RESOURCES,
            blank=True,
            default='0',
            help_text='Resources the planet demands',
        ),
        5
    )
    planet_demand_resources_price = ArrayField(
        models.IntegerField(),
        5
    )
    planet_supply_resources = ArrayField(
        models.CharField(
            max_length=1,
            choices=RESOURCES,
            blank=True,
            default='0',
            help_text='Resources the planet supplies',
        ),
        5
    )
    planet_supply_resources_price = ArrayField(
        models.IntegerField(),
        5
    )

    radius_x = models.IntegerField()
    radius_y = models.IntegerField()
    offset = models.FloatField()

    planet_number = models.IntegerField(default=0)

    add_demand_resource = models.CharField(
        max_length=1,
        choices=RESOURCES,
        blank=True,
        default='0',
        help_text='Resources the planet supplies',
    )
    add_demand_resource_price = models.IntegerField(default=0)
    add_demand_resource_time = models.IntegerField(default=0)

    objects = PlanetManager()

    def get_json(self):
        planet_data = {
            'name': self.name,
            'colour': self.colour,
            'number_of_hexes': self.number_of_hexes,
            'position_of_hexes': self.position_of_hexes,
            'current_position': self.current_position,
            'planet_demand_resources': self.planet_demand_resources,
            'planet_demand_resources_price': self.planet_demand_resources_price,
            'planet_supply_resources': self.planet_supply_resources,
            'planet_supply_resources_price': self.planet_supply_resources_price,
            'radius_x': self.radius_x,
            'radius_y': self.radius_y,
            'offset': self.offset,
            'planet_number': self.planet_number,
            'add_demand_resource': self.add_demand_resource,
            'add_demand_resource_price': self.add_demand_resource_price,
            'add_demand_resource_time': self.add_demand_resource_time
        }
        return planet_data

    def __str__(self):
        return str("name: {planet.name}, "
                   "number_of_hexes: {planet.number_of_hexes}, "
                   "current_position: {planet.current_position}, "
                   "planet_demand_resources: {planet.planet_demand_resources}, "
                   "planet_demand_resources_price: {planet.planet_demand_resources_price}, "
                   "planet_supply_resources: {planet.planet_supply_resources}, "
                   "planet_supply_resources_price: {planet.planet_supply_resources_price}".format(planet=self))


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
            has_passed=False,
            points=0
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
            has_passed=has_passed,
            points=points
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
    points = models.IntegerField(default=0)

    objects = PlayerManager()

    def get_json(self):
        player_data = {
            'resources': self.resources,
            'money': self.money,
            'ship_position': self.ship_position,
            'last_move': self.last_move,
            'time_spent': self.time_spent,
            'colour': self.colour,
            'ship_offset': self.ship_offset,
            'player_number': self.player_number,
            'has_passed': self.has_passed,
            'points': self.points
        }
        return player_data

    def __str__(self):
        return f"User {self.user}"


class GameManager(models.Manager):
    def create_game(
            self,
            game_name="",
            number_of_players=1,
            next_move_number=gamesettings.FIRST_MOVE_NUMBER,
            game_state='w',
            planet_rotation_event_time=gamesettings.PLANET_ROTATION_TIME,
            planet_rotation_event_move=gamesettings.PLANET_ROTATION_MOVE,
            offer_demand_event_time=gamesettings.OFFER_DEMAND_EVENT_TIMES[0],
            offer_demand_event_move=gamesettings.OFFER_DEMAND_EVENT_MOVE,
            planet_influence_track=None,
            resource_limit=9,
            midgame_scoring=False,
            midgame_scoring_event_time=gamesettings.MIDGAME_SCORING_TIME,
            midgame_scoring_event_move=gamesettings.MIDGAME_SCORING_MOVE,
            add_demand=False,
            add_demand_event_time=gamesettings.ADD_DEMAND_TIME,
            add_demand_event_move=gamesettings.ADD_DEMAND_MOVE,
            finish_time=gamesettings.FINISH_TIME,
            start_influence=gamesettings.START_INFLUENCE
    ):
        if planet_influence_track is None:
            planet_influence_track = [[start_influence]*4 for _ in range(5)]
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
            resource_limit=resource_limit,
            midgame_scoring=midgame_scoring,
            midgame_scoring_event_move=midgame_scoring_event_move,
            midgame_scoring_event_time=midgame_scoring_event_time,
            add_demand=add_demand,
            add_demand_event_time=add_demand_event_time,
            add_demand_event_move=add_demand_event_move,
            finish_time=finish_time
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

    midgame_scoring = models.BooleanField(default=False)
    midgame_scoring_event_time = models.IntegerField(default=50)
    midgame_scoring_event_move = models.IntegerField(default=-10)

    add_demand = models.BooleanField(default=False)
    add_demand_event_time = models.IntegerField(default=17)
    add_demand_event_move = models.IntegerField(default=-8)

    finish_time = models.IntegerField(default=100)

    objects = GameManager()

    def get_absolute_url(self):
        """Returns the url to access a game."""
        return reverse('game_detail', args=[str(self.id)])

    def is_active(self):
        """Return True if game_state is running otherwise False"""
        return (self.game_state == 'r')

    def get_users(self):
        user_group_set = set()
        for player in self.players.all():
            user_group_set.add(player.user)

        return user_group_set

    def get_active_player(self):
        return move.get_active_player(self.players.all(), self.finish_time)

    def get_active_user(self):
        return self.get_active_player().user

    def get_json(self, players=None, planets=None):
        if players is None:
            players = self.players.all().order_by('player_number')
        if planets is None:
            planets = self.planets.all().order_by('planet_number')

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
            'planet_influence_track': self.planet_influence_track,
            'midgame_scoring': self.midgame_scoring,
            'midgame_scoring_event_move': self.midgame_scoring_event_move,
            'midgame_scoring_event_time': self.midgame_scoring_event_time,
            'add_demand': self.add_demand,
            'add_demand_event_time': self.add_demand_event_time,
            'add_demand_event_move': self.add_demand_event_move,
            'finish_time': self.finish_time
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
