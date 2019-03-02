from django.contrib import admin
#from django.contrib.postgres.forms import SplitArrayField, SimpleArrayField
from django.forms import MultiWidget
from django.forms import widgets
from django import forms
import spacetrading

# Register your models here.

class Array2dWidget(MultiWidget):
    def __init__(self, base_widget, _number_1, _number_2, attrs=None):
        self.number_1 = _number_1
        self.number_2 = _number_2
        widgets = [base_widget] * _number_1 * _number_2
        super().__init__(widgets, attrs)

    def __str__(self):
        print("number1: {}, number2: {}".format(self.number_1, self.number_2))

    def decompress(self, value):
        print("decompress")
        values = value.split(",")
        print(values)
        return values

    def value_from_datadict(self, data, files, name):
        print('value_from')
        values = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        print(values)
        result = []
        for index in range(self.number_2):
            print(index)
            print(self.number_1*index)
            result.append(values[self.number_1*index:(index+1)*self.number_1])
        print(result)
        return result


class GameAdminForm(forms.ModelForm):
    class Meta:
        model = spacetrading.models.Game
        widgets = {
            'planet_influence_track': Array2dWidget(
                    widgets.NumberInput, 4, 5
            ),
        }
        fields = '__all__'

class GameAdmin(admin.ModelAdmin):
    form = GameAdminForm

admin.site.register(spacetrading.models.Game, GameAdmin)
admin.site.register(spacetrading.models.Planet)
admin.site.register(spacetrading.models.Player)
