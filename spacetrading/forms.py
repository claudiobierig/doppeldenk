"""
forms needed to play spacetrading
"""

from django import forms
from django.utils.safestring import mark_safe
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
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    midgame_scoring = forms.BooleanField(
        label="Midgame scoring",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    add_demand = forms.BooleanField(
        label="Add demand resources throughout the game",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class Move(forms.Form):
    """
    Form to make a move
    """
    coord_q = forms.IntegerField(
        label="Coordinate q", min_value=-20, max_value=20,
        widget=forms.HiddenInput(), initial=0,
        required=False
    )
    coord_r = forms.IntegerField(
        label="Coordinate r", min_value=-20, max_value=20,
        widget=forms.HiddenInput(), initial=0,
        required=False
    )

    RESOURCE_TO_SYMBOL = {
        "1": "red_cross",
        "2": "radioactive",
        "3": "food",
        "4": "water",
        "5": "building_resource"
    }
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

    def __init__(self, *args, **kwargs):
        active_planet = args[0].get("active_planet", None)
        active_player = args[0].get("active_player", None)
        symbols = args[0].get("symbols", None)
        if active_planet is None:
            planet_supply_resources = []
            planet_demand_resources = []
            planet_supply_resources_price = []
            planet_demand_resources_price = []
            influence = False
        else:
            planet_supply_resources = active_planet.planet_supply_resources
            planet_demand_resources = active_planet.planet_demand_resources
            planet_supply_resources_price = active_planet.planet_supply_resources_price
            planet_demand_resources_price = active_planet.planet_demand_resources_price
            influence = True

        if active_player is None or active_player.time_spent < 0:
            time = False
        else:
            time = True
        
        for direction, mapping, resources, cost in [
                ("Sell", move.PLANET_DEMAND_MAPPING, planet_demand_resources, planet_demand_resources_price),
                ("Buy", move.PLANET_SUPPLY_MAPPING, planet_supply_resources, planet_supply_resources_price)
                
            ]:
            for resource in range(1, 6):
                fieldname = mapping[str(resource)]
                if str(resource) in resources:
                    self.base_fields[fieldname] = forms.IntegerField(
                        label=mark_safe("{} {}".format(direction, symbols[self.RESOURCE_TO_SYMBOL[str(resource)]])),
                        max_value=9, min_value=0,
                        widget=forms.Select(
                            choices=self.CHOICES,
                            attrs={
                                'onchange': 'refreshChoices()',
                                'class': "form-control form-control-sm"
                            }
                        ),
                        initial=0,
                        help_text="{}".format(cost[resources.index(str(resource))])
                    )
                else:
                    self.base_fields[fieldname] = forms.IntegerField(
                        widget=forms.HiddenInput(),
                        required=False,
                        initial=0
                    )


        if influence:
            self.base_fields["buy_influence"] = forms.IntegerField(
                label=mark_safe("Buy {}".format(symbols["influence"])),
                min_value=0, max_value=99,
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
                label=mark_safe("Spend {}".format(symbols["time"])),
                min_value=0, max_value=100,
                widget=forms.NumberInput(
                    attrs={
                        'onchange': 'timeChanged()',
                        'class': 'form-control form-control-sm'
                    }
                ),
                initial=0,
                required=False
            )
        else:
            self.base_fields["spend_time"] = forms.IntegerField(
                widget=forms.HiddenInput(),
                required=False,
                initial=0
            )


        super(Move, self).__init__(*args, **kwargs)
