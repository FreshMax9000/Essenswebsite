from django import forms
from django.forms.models import  modelformset_factory

from .models import Foodplan
from .models import Grocerie
from .models import Recipe
from .models import Ingredient


class FoodplanForm(forms.ModelForm):
    days = forms.IntegerField(initial=5, max_value=14, min_value=1, label="Anzahl an Tagen: ")

    class Meta:
        model = Foodplan
        fields = ['days']

class CreateIngredientForm(forms.ModelForm):
    quantity = forms.NumberInput()
    grocerie = forms.ModelChoiceField(queryset=Grocerie.objects.all(), empty_label="wählen", label="Zutat:", localize=True)

    class Meta:
        model = Ingredient
        fields = ('quantity', 'grocerie')



class CreateRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation', 'work_time')

IngredientFormset = modelformset_factory(Ingredient, form=CreateIngredientForm)
