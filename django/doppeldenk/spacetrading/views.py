from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView

from spacetrading import models
#from create_svg import generate_player_board
from spacetrading import forms

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
        form = forms.NewGame(request.POST)
        if form.is_valid():
            models.create_game(
                form.cleaned_data['name'],
                form.cleaned_data['number_of_players'],
                request.user
            )
            if form.cleaned_data['number_of_players'] is 1:
                return HttpResponseRedirect(reverse('active_games'))
            else:
                return HttpResponseRedirect(reverse('open_games'))
    else:
        form = forms.NewGame(initial={'name': '', 'number_of_players': 1})

    context = {
        'form': form
    }
    return render(request, 'spacetrading/create_game.html', context=context)

class ActiveGameListView(LoginRequiredMixin, generic.ListView):
    model = models.Game
    context_object_name = 'game_list'   # your own name for the list as a template variable
    template_name = 'spacetrading/game_list.html'
    paginate_by = 10

    def get_queryset(self):
        games = models.Game.objects.filter(players__user=self.request.user).filter(game_state='r')
        
        return games

class OpenGameListView(LoginRequiredMixin, generic.ListView):
    model = models.Game
    context_object_name = 'game_list'   # your own name for the list as a template variable
    template_name = 'spacetrading/game_list.html'
    paginate_by = 10

    def get_queryset(self):
        games = models.Game.objects.filter(game_state='w')
        return games

class GameDetailView(generic.DetailView):
    model = models.Game
