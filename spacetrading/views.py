import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib import messages

from spacetrading import models
#from create_svg import generate_player_board
from spacetrading import forms
from spacetrading.create_svg import generate_gameboard, generate_planet_market, generate_player_boards, generate_trade_modal, generate_plain_symbols, generate_influence_track
from spacetrading.logic import move

@login_required
def create_game(request):
    """Create a game"""
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = forms.NewGame(request.POST)
        if form.is_valid():
            models.create_game(
                form.cleaned_data['name'],
                form.cleaned_data['number_of_players'],
                form.cleaned_data['play_all_players'],
                request.user
            )

            return HttpResponseRedirect(request.path_info)
    else:
        form = forms.NewGame(initial={'name': '', 'number_of_players': 1})

    context = {
        'form': form
    }
    return render(request, 'spacetrading/create_game.html', context=context)

@login_required
def next_game(request):
    """go to next game where user is avtive"""
    games = models.Game.objects.filter(players__user=request.user).filter(game_state='r').order_by('id')
    next = get_next_game(games, request.user)
    if next:
        return HttpResponseRedirect(reverse('game_detail', args=[next.id]))
    return HttpResponseRedirect(reverse('active_games'))

def get_next_game(queryset, user):
    for game in queryset:
        players = game.players.all().order_by('player_number')
        active_player = move.get_active_player(players)
        if active_player.user == user:
            return game
    return False

def rules(request):
    return render(request, 'spacetrading/rules.html')

class ActiveGameListView(LoginRequiredMixin, generic.ListView):
    model = models.Game
    context_object_name = 'game_list'   # your own name for the list as a template variable
    template_name = 'spacetrading/game_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = "Active Games"
        context['joinable'] = False
        return context

    def get_queryset(self):
        games = models.Game.objects.filter(players__user=self.request.user).distinct().filter(game_state='r').order_by('id')
        return games

class OpenGameListView(LoginRequiredMixin, generic.ListView):
    model = models.Game
    context_object_name = 'game_list'   # your own name for the list as a template variable
    template_name = 'spacetrading/game_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = "Open Games"
        context['joinable'] = True
        return context

    def get_queryset(self):
        games = models.Game.objects.filter(game_state='w').order_by('id')
        return games
    
    def post(self, request, *args, **kwargs):
        for key, _ in request.POST.items():
            if(re.match("join_\\d+", key)):
                primary_key_game = key[5:]
                models.join_game(primary_key_game, request.user)

        return HttpResponseRedirect(self.request.path_info)

class GameDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = models.Game
    form_class = forms.Move

    def get_next(self, game_instance):
        all_games = models.Game.objects.filter(players__user=self.request.user).filter(game_state='r').order_by('id')
        game_gt = all_games.filter(id__gt=game_instance.id)
        game = get_next_game(game_gt, self.request.user)
        if game:
            return game
        game_lt = all_games.filter(id__lt=game_instance.id)
        game = get_next_game(game_lt, self.request.user)
        if game:
            return game

        return False


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        game_instance = super().get_object()
        planets = game_instance.planets.all().order_by('number_of_hexes')
        players = game_instance.players.all().order_by('player_number')
        active_player = move.get_active_player(players)
        active_planet = get_active_planet(active_player, planets)
        colour_active_planet = "#FFF"
        if active_planet is not None:
            colour_active_planet = active_planet.colour
        user_active = active_player is not None and active_player.user == self.request.user
        symbols = generate_plain_symbols.draw_symbols()
        context['nextgame'] = self.get_next(game_instance)
        context['gameboard'] = generate_gameboard.draw_gameboard(game_instance, planets, players, user_active)
        context['influence_tracks'] = generate_influence_track.draw_influence_tracks(game_instance, planets, players)
        context['planet_market'] = generate_planet_market.draw_planet_market(planets)
        context['player_boards'] = generate_player_boards.draw_player_boards(players, game_instance)
        context['trade_modal'] = generate_trade_modal.draw_trade_modal(players, planets)
        context['user_active'] = user_active
        context['coin'] = symbols['coin']
        context["red_cross"] = symbols["red_cross"]
        context["radioactive"] = symbols["radioactive"]
        context["food"] = symbols["food"]
        context["water"] = symbols["water"]
        context["building_resource"] = symbols["building_resource"]
        context["influence"] = symbols["influence"]
        context["can_trade"] = active_planet is not None
        context["colour_active_planet"] = colour_active_planet
        context["buy_resources"] = get_trade_resources("buy", active_planet)
        context["sell_resources"] = get_trade_resources("sell", active_planet)
        context["cost_buy_resources"] = get_cost_trade_resources("buy", active_planet)
        context["cost_sell_resources"] = get_cost_trade_resources("sell", active_planet)
        context["influence_so_far"] = get_influence_so_far(game_instance, planets, active_player, active_planet)
        return context

    def post(self, request, *args, **kwargs):
        form = forms.Move(request.POST)
        if form.is_valid():
            game_instance = super().get_object()
            active_player = game_instance.get_active_player()
            if request.user == active_player.user:
                if 'Regular' in form.data:
                    try:
                        move.move(game_instance, form.cleaned_data)
                    except move.MoveError as exception:
                        messages.error(request, 'Error: {}.'.format(exception))
                elif 'Pass' in form.data:
                    move.pass_game(game_instance)

        return HttpResponseRedirect(self.request.path_info)

def get_trade_resources(direction, planet):
    if planet is None:
        return []
    if direction == "sell":
        return planet.sell_resources
    elif direction == "buy":
        return planet.buy_resources

def get_cost_trade_resources(direction, planet):
    if planet is None:
        return []
    if direction == "sell":
        return planet.cost_sell_resource
    elif direction == "buy":
        return planet.cost_buy_resource

def get_active_planet(player, planets):
    if player is None:
        return None
    for planet in planets:
        if player.ship_position == planet.position_of_hexes[planet.current_position]:
            return planet
    return None

def get_influence_so_far(game, planets, active_player, active_planet):
    if active_planet is None:
        return ""
    for index, planet in enumerate(planets):
        if planet == active_planet:
            return str(game.planet_influence_track[index][active_player.player_number])
