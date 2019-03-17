from django.contrib import admin
from django.forms import MultiWidget
from django.forms import widgets
from django import forms
import spacetrading

# Register your models here.

class Array2dWidget(MultiWidget):
    template_name = "spacetrading/array2d_widget.html"

    def __init__(self, base_widget, _inner_array_size, _outer_array_size, attrs=None):
        self.inner_array_size = _inner_array_size
        self.outer_array_size = _outer_array_size
        my_widgets = [base_widget] * _inner_array_size * _outer_array_size
        super().__init__(my_widgets, attrs)

    def decompress(self, value):
        values = value.split(",")
        return values

    def value_from_datadict(self, data, files, name):
        values = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        result = []
        for index in range(self.outer_array_size):
            subresult = []
            for sub_index in range(self.inner_array_size):
                if values[self.inner_array_size*index + sub_index]:
                    subresult.append(values[self.inner_array_size*index + sub_index])
                else:
                    break
            
            if subresult:
                result.append(subresult)
            else:
                break

        return result

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)
        context["widget"]["inner_array_size"] = self.inner_array_size
        context["widget"]["outer_array_size"] = self.outer_array_size
        return context


class GameAdminForm(forms.ModelForm):
    class Meta:
        model = spacetrading.models.Game
        widgets = {
            'planet_influence_track': Array2dWidget(
                widgets.NumberInput, 4, 5
            ),
        }
        fields = '__all__'

class PlanetAdminForm(forms.ModelForm):
    class Meta:
        model = spacetrading.models.Planet
        widgets = {
            'position_of_hexes': Array2dWidget(
                widgets.NumberInput, 2, 20
            ),
        }
        fields = '__all__'

class GameAdmin(admin.ModelAdmin):
    form = GameAdminForm

class PlanetAdmin(admin.ModelAdmin):
    form = PlanetAdminForm

admin.site.register(spacetrading.models.Game, GameAdmin)
admin.site.register(spacetrading.models.Planet, PlanetAdmin)
admin.site.register(spacetrading.models.Player)
