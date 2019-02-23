from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView

import re

from spacetrading import models
#from create_svg import generate_player_board
from spacetrading import forms
from spacetrading.create_svg import generate_gameboard, generate_planet_market, generate_player_boards

@login_required
def index(request):
    """View function for home page of site."""
    svg_string = "hello"#generate_player_board.main()
    context = {
        'num_books': "1",
        'svg': svg_string
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'spacetrading/index.html', context=context)

@login_required
def create_game(request):
    """Create a game"""
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        print(request.POST)
        form = forms.NewGame(request.POST)
        print(form.data)
        if form.is_valid():
            models.create_game(
                form.cleaned_data['name'],
                form.cleaned_data['number_of_players'],
                request.user
            )
            if form.cleaned_data['number_of_players'] == 1:
                return HttpResponseRedirect(reverse('active_games'))

            return HttpResponseRedirect(reverse('open_games'))
    else:
        form = forms.NewGame(initial={'name': '', 'number_of_players': 1})

    context = {
        'form': form
    }
    return render(request, 'spacetrading/create_game.html', context=context)

@login_required
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
        games = models.Game.objects.filter(players__user=self.request.user).filter(game_state='r')
        
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
        games = models.Game.objects.filter(game_state='w')
        return games
    
    def post(self, request, *args, **kwargs):
        for key, _ in request.POST.items():
            if(re.match("join_\\d+", key)):
                primary_key_game = key[5:]
                print("Want to join game " + primary_key_game)
                models.join_game(primary_key_game, request.user)

        return HttpResponseRedirect(reverse('open_games'))

class GameDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Game

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        game_instance = super().get_object()
        planets = game_instance.planets.all()
        players = game_instance.players.all()
        # Add in a QuerySet of all the books
        context['gameboard'] = generate_gameboard.draw_gameboard(game_instance)
        context['planet_market'] = generate_planet_market.draw_planet_market(planets)
        context['player_boards'] = generate_player_boards.draw_player_boards(players)
        return context
