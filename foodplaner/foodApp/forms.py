from django import forms

from .models import Foodplan


class FoodplanForm(forms.ModelForm):
    days = forms.IntegerField(initial=5, max_value=14, min_value=1, label="Anzahl an Tagen: ")
    daytime_choices = {(1, 'Mittag & Abend'), (2, 'Mittag'), (3, 'Abend')}
    select_daytime = forms.ChoiceField(choices=daytime_choices, initial=1, label="Tageszeit wählen:", required=False, localize=True)

    class Meta:
        model = Foodplan
        fields = ['days', 'select_daytime']
