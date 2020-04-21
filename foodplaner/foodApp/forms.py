"""
a form is a collection of elements inside <form>...</form> that allow a visitor to do things like enter text, 
select options, manipulate objects or controls, and so on, and then send that information back to the server.
As well as its <input> elements, a form must specify two things:

where: the URL to which the data corresponding to the user’s input should be returned
how: the HTTP method the data should be returned by
"""

from django import forms

from .models import Foodplan


class FoodplanForm(forms.ModelForm):
    days = forms.IntegerField(initial=5, max_value=14, min_value=1, label="Anzahl an Tagen: ")

    class Meta:
        model = Foodplan
        fields = ['days']
