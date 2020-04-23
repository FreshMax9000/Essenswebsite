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


class CreateGroceryForm(forms.ModelForm):
    class Meta:
        model = Grocerie
        fields = ('name', 'unit')
        labels = {
            'name': 'Name: ',
            'unit': 'Einheit (g, ml, mg, Kg, ...): ',
        }


class CreateIngredientForm(forms.ModelForm):
    quantity = forms.DecimalField(min_value=0, label='Menge: ')
    grocerie = forms.ModelChoiceField(queryset=Grocerie.objects.all().order_by('name'), empty_label=" --- ", label="Zutat: ", localize=True)

    class Meta:
        model = Ingredient
        fields = ('quantity', 'grocerie')


class CreateRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation', 'work_time')
        labels = {
            'title': 'Titel',
            'description': 'Beschreibung: ',
            'preparation': 'Zubereitung: ',
            'work_time': 'Zubereitungszeit: ',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hier Titel eingeben'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Hier Kurzbeschreibung eingeben'
            }),
            'preparation': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Hier die Zubereitung beschreiben'
            }),
            'work_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
        }


IngredientFormset = modelformset_factory(Ingredient, form=CreateIngredientForm)
