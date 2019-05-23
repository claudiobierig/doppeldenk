import json
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
from spacetrading.create_svg import generate_gameboard, generate_planet_market, generate_player_boards, generate_trade_modal, generate_plain_symbols
from spacetrading.logic import move, initialize


@login_required
def create_game(request):
    """Create a game"""
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = forms.NewGame(request.POST)
        if form.is_valid():
            initialize.create_game(
                form.cleaned_data,
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
    game = models.Game.objects.next(request.user)
    if game:
        return HttpResponseRedirect(reverse('game_detail', args=[game.id]))
    return HttpResponseRedirect(reverse('active_games'))


def rules(request):
    return render(request, 'spacetrading/rules.html')


class ActiveGameListView(LoginRequiredMixin, generic.ListView):
    model = models.Game
    context_object_name = 'game_list'
    template_name = 'spacetrading/game_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = "Active Games"
        context['joinable'] = False
        return context

    def get_queryset(self):
        games = models.Game.objects.filter(
            players__user=self.request.user).distinct().filter(game_state='r').order_by('id')
        return games


class OpenGameListView(LoginRequiredMixin, generic.ListView):
    model = models.Game
    # your own name for the list as a template variable
    context_object_name = 'game_list'
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
                initialize.join_game(primary_key_game, request.user)

        return HttpResponseRedirect(self.request.path_info)


class GameDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = models.Game
    form_class = forms.Move

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        game_instance = super().get_object()
        planets = game_instance.planets.all().order_by('number_of_hexes')
        players = game_instance.players.all().order_by('player_number')
        active_player = move.get_active_player(players)

        user_active = active_player is not None and active_player.user == self.request.user
        symbols = generate_plain_symbols.draw_symbols()
        context['game_data'] = json.dumps(game_instance.get_json(), indent=4)
        context['nextgame'] = models.Game.objects.next(
            self.request.user, game_instance.id)
        context['gameboard'] = generate_gameboard.draw_gameboard(
            game_instance, planets, players, user_active)
        context['planet_market'] = generate_planet_market.draw_planet_market(
            game_instance, planets, players)
        context['player_boards'] = generate_player_boards.draw_player_boards(
            players, game_instance)

        context["red_cross"] = symbols["red_cross"]
        context["radioactive"] = symbols["radioactive"]
        context["food"] = symbols["food"]
        context["water"] = symbols["water"]
        context["building_resource"] = symbols["building_resource"]
        context["influence"] = symbols["influence"]
        context["time"] = symbols["time"]

        context['user_active'] = user_active

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
