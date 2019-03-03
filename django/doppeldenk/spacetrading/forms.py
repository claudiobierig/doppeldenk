from django import forms
from spacetrading import models

class NewGame(forms.Form):
    name = forms.CharField(label="Game Name")
    number_of_players = forms.IntegerField(label="Number of Players", max_value=4, min_value=1)

class Move(forms.Form):
    coord_q = forms.IntegerField(label="Coordinate q", min_value=-20, max_value=20,
        widget=forms.HiddenInput(), initial=0)
    coord_r = forms.IntegerField(label="Coordinate r", min_value=-20, max_value=20,
        widget=forms.HiddenInput(), initial=0)

    sell_resource_1 = forms.IntegerField(label="Sell resource 1", max_value=9, min_value=0,
        widget=forms.HiddenInput(), initial=0)
    sell_resource_2 = forms.IntegerField(label="Sell resource 2", max_value=9, min_value=0,
        widget=forms.HiddenInput(), initial=0)
    sell_resource_3 = forms.IntegerField(label="Sell resource 3", max_value=9, min_value=0,
        widget=forms.HiddenInput(), initial=0)
    sell_resource_4 = forms.IntegerField(label="Sell resource 4", max_value=9, min_value=0,
        widget=forms.HiddenInput(), initial=0)
    sell_resource_5 = forms.IntegerField(label="Sell resource 5", max_value=9, min_value=0,
        widget=forms.HiddenInput(), initial=0)

    buy_resource_1 = forms.IntegerField(label="Buy resource 1", max_value=9, min_value=0,
        widget=forms.HiddenInput(), initial=0)
    buy_resource_2 = forms.IntegerField(label="Buy resource 2", max_value=9, min_value=0,
        widget=forms.HiddenInput(), initial=0)
    buy_resource_3 = forms.IntegerField(label="Buy resource 3", max_value=9, min_value=0,
        widget=forms.HiddenInput(), initial=0)
    buy_resource_4 = forms.IntegerField(label="Buy resource 4", max_value=9, min_value=0,
        widget=forms.HiddenInput(), initial=0)
    buy_resource_5 = forms.IntegerField(label="Buy resource 5", max_value=9, min_value=0,
        widget=forms.HiddenInput(), initial=0)

    buy_influence = forms.IntegerField(label="Buy influence", min_value=0, max_value=99,
        widget=forms.HiddenInput(), initial=0)
