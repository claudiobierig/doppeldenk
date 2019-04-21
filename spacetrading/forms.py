from django import forms
from spacetrading import models

class NewGame(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="Game Name",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Game Name'})
    )
    number_of_players = forms.IntegerField(
        label="Number of Players",
        max_value=4,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    play_all_players = forms.BooleanField(
        label="Play all Players",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class Move(forms.Form):
    coord_q = forms.IntegerField(
        label="Coordinate q", min_value=-20, max_value=20,
        widget=forms.HiddenInput(), initial=0
    )
    coord_r = forms.IntegerField(
        label="Coordinate r", min_value=-20, max_value=20,
        widget=forms.HiddenInput(), initial=0
    )

    CHOICES = (
        ('0', 0),
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
        ('6', 6),
        ('7', 7),
        ('8', 8),
        ('9', 9),
    )
    sell_resource_1 = forms.IntegerField(
        label="Sell resource 1", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )
    sell_resource_2 = forms.IntegerField(
        label="Sell resource 2", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )
    sell_resource_3 = forms.IntegerField(
        label="Sell resource 3", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )
    sell_resource_4 = forms.IntegerField(
        label="Sell resource 4", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )
    sell_resource_5 = forms.IntegerField(
        label="Sell resource 5", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )

    buy_resource_1 = forms.IntegerField(
        label="Buy resource 1", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )
    buy_resource_2 = forms.IntegerField(
        label="Buy resource 2", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )
    buy_resource_3 = forms.IntegerField(
        label="Buy resource 3", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )
    buy_resource_4 = forms.IntegerField(
        label="Buy resource 4", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )
    buy_resource_5 = forms.IntegerField(
        label="Buy resource 5", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )

    buy_influence = forms.IntegerField(
        label="Buy influence", min_value=0, max_value=99,
        widget=forms.Select(
            choices=CHOICES,
            attrs={'onchange': 'refreshChoices()'}
        ),
        initial=0
    )
