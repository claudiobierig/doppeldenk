from django import forms
from spacetrading import models

class NewGame(forms.Form):
    name = forms.CharField(label="Game Name")
    number_of_players = forms.IntegerField(label="Number of Players", max_value=4, min_value=1)
