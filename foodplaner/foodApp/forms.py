"""
Module is used to provide forms to gather formatted user input.
"""
from django import forms

from .models import Foodplan


class FoodplanForm(forms.ModelForm):
    """
    Reads user input about how many days the foodplan should be generated.
    """
    days = forms.IntegerField(initial=5, max_value=14, min_value=1, label="Anzahl an Tagen: ")

    class Meta:
        model = Foodplan
        fields = ['days']
