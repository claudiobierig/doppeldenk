from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

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

class GameListView(LoginRequiredMixin, generic.ListView):
    model = models.Game
    context_object_name = 'game_list'   # your own name for the list as a template variable
    template_name = 'spacetrading/game_list.html'

    def get_queryset(self):
        games = set()
        for player in models.Player.objects.filter(user=self.request.user).prefetch_related('game'):
            games.add(player.game)
        ##return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        
        #games = models.Game.objects.
        return games
    #queryset = models.Game.objects #.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    #template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
