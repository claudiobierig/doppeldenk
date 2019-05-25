"""
forms needed to play spacetrading
"""

from django import forms
from spacetrading.logic import move


class NewGame(forms.Form):
    """
    Form to create a new spacetrading game
    """
    name = forms.CharField(
        max_length=100,
        required=False,
        label="Game Name",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Game Name'})
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
    resource_limit = forms.IntegerField(
        label="Maximal number of one resource",
        max_value=15,
        min_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class Move(forms.Form):
    """
    Form to make a move
    """
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
            attrs={
                'onchange': 'refreshChoices()',
                'class': "form-control form-control-sm"
            }
        ),
        initial=0
    )
    sell_resource_2 = forms.IntegerField(
        label="Sell resource 2", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'onchange': 'refreshChoices()',
                'class': "form-control form-control-sm"
            }
        ),
        initial=0
    )
    sell_resource_3 = forms.IntegerField(
        label="Sell resource 3", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'onchange': 'refreshChoices()',
                'class': "form-control form-control-sm"
            }
        ),
        initial=0
    )
    sell_resource_4 = forms.IntegerField(
        label="Sell resource 4", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'onchange': 'refreshChoices()',
                'class': "form-control form-control-sm"
            }
        ),
        initial=0
    )
    sell_resource_5 = forms.IntegerField(
        label="Sell resource 5", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'onchange': 'refreshChoices()',
                'class': "form-control form-control-sm"
            }
        ),
        initial=0
    )

    buy_resource_1 = forms.IntegerField(
        label="Buy resource 1", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'onchange': 'refreshChoices()',
                'class': "form-control form-control-sm"
            }
        ),
        initial=0
    )
    buy_resource_2 = forms.IntegerField(
        label="Buy resource 2", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'onchange': 'refreshChoices()',
                'class': "form-control form-control-sm"
            }
        ),
        initial=0
    )
    buy_resource_3 = forms.IntegerField(
        label="Buy resource 3", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'onchange': 'refreshChoices()',
                'class': "form-control form-control-sm"
            }
        ),
        initial=0
    )
    buy_resource_4 = forms.IntegerField(
        label="Buy resource 4", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'onchange': 'refreshChoices()',
                'class': "form-control form-control-sm"
            }
        ),
        initial=0
    )
    buy_resource_5 = forms.IntegerField(
        label="Buy resource 5", max_value=9, min_value=0,
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'onchange': 'refreshChoices()',
                'class': "form-control form-control-sm"
            }
        ),
        initial=0
    )

    def __init__(self, *args, **kwargs):
        active_planet = args[0].get("active_planet", None)
        active_player = args[0].get("active_player", None)
        if active_planet is None:
            sell_resources = []
            buy_resources = []
            influence = False
        else:
            sell_resources = active_planet.sell_resources
            buy_resources = active_planet.buy_resources
            influence = True

        if active_player is None or active_player.time_spent < 0:
            time = False
        else:
            time = True

        if influence:
            self.base_fields["buy_influence"] = forms.IntegerField(
                label="Buy influence", min_value=0, max_value=99,
                widget=forms.Select(
                    choices=self.CHOICES,
                    attrs={
                        'onchange': 'refreshChoices()',
                        'class': "form-control form-control-sm"
                    }
                ),
                initial=0
            )
        else:
            self.base_fields["buy_influence"] = forms.IntegerField(
                widget=forms.HiddenInput(),
                required=False,
                initial=0
            )
        
        if time:
            self.base_fields["spend_time"] = forms.IntegerField(
                label="Spend time", min_value=0, max_value=100,
                widget=forms.NumberInput(
                    attrs={'class': 'form-control form-control-sm'}),
                initial=0
            )
        else:
            self.base_fields["spend_time"] = forms.IntegerField(
                widget=forms.HiddenInput(),
                required=False,
                initial=0
            )
        
        for direction, mapping, resources in [
                ("Buy", move.BUY_MAPPING, buy_resources),
                ("Sell", move.SELL_MAPPING, sell_resources)
            ]:
            for resource in range(1, 6):
                fieldname = mapping[str(resource)]
                if str(resource) in resources:
                    self.base_fields[fieldname] = forms.IntegerField(
                        label="{} resource {}".format(direction, resource), max_value=9, min_value=0,
                        widget=forms.Select(
                            choices=self.CHOICES,
                            attrs={
                                'onchange': 'refreshChoices()',
                                'class': "form-control form-control-sm"
                            }
                        ),
                        initial=0
                    )
                else:
                    self.base_fields[fieldname] = forms.IntegerField(
                        widget=forms.HiddenInput(),
                        required=False,
                        initial=0
                    )

        super(Move, self).__init__(*args, **kwargs)
