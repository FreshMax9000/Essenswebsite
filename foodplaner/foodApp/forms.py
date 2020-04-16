from django import forms

from .models import Foodplan


class FoodplanForm(forms.ModelForm):
    days = forms.IntegerField(initial=5, max_value=14, min_value=1, label="Anzahl an Tagen: ")

    class Meta:
        model = Foodplan
        fields = ['days']
