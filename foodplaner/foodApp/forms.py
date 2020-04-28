from django import forms
from django.forms.models import  modelformset_factory

from .models import Foodplan
from .models import Grocery
from .models import Recipe
from .models import Ingredient
from .models import Commentary


class FoodplanForm(forms.ModelForm):
    days = forms.IntegerField(initial=5, max_value=14, min_value=1, label="Anzahl an Tagen: ")
    daytime_choices = {(1, 'Mittag & Abend'), (2, 'Mittag'), (3, 'Abend')}
    select_daytime = forms.ChoiceField(choices=daytime_choices, initial=1, label="Tageszeit wählen:", required=False, localize=True)

    class Meta:
        model = Foodplan
        fields = ['days', 'select_daytime']

class CommentaryForm(forms.ModelForm):
    title = forms.CharField(max_length=50, label='Titel: ')
    title.widget = forms.TextInput(attrs={'placeholder': 'Hier Titel eingeben'})
    content = forms.CharField(label='Kommentar: ')
    content.widget = forms.Textarea(attrs={'placeholder': 'Hier den Kommentar einfügen'})
    rating = forms.IntegerField(min_value=1, max_value=10, label='Bewertung (1-10): ')

    class Meta:
        model = Commentary
        fields = ['title', 'content', 'rating']


class CreateGroceryForm(forms.ModelForm):
    name = forms.CharField(max_length=30, label='Name: ')
    unit = forms.CharField(max_length=15, label='Einheit (g, ml, mg, Kg, ...): ')

    class Meta:
        model = Grocery
        fields = ('name', 'unit')


class CreateIngredientForm(forms.ModelForm):
    quantity = forms.DecimalField(min_value=0.1, required=False, label='Menge: ')
    grocery = forms.ModelChoiceField(queryset=Grocery.objects.all().order_by('name'), empty_label=" --- ", required=False, label="Zutat: ")

    class Meta:
        model = Ingredient
        fields = ('quantity', 'grocery')


class RecipeForm(forms.ModelForm):
    title = forms.CharField(max_length=50, label='Titel: ')
    title.widget = forms.TextInput(attrs={'placeholder': 'Hier Titel eingeben'})
    description = forms.CharField(max_length=100, required=False, label='Beschreibung: ')
    description.widget = forms.TextInput(attrs={'placeholder': 'Hier Kurzbeschreibung eingeben'})
    preparation = forms.CharField(label='Zubereitung: ')
    preparation.widget = forms.Textarea(attrs={'placeholder': 'Hier die Zubereitung beschreiben'})
    work_time = forms.IntegerField(min_value=1, label='Zubereitungszeit: ')
    reviewed = forms.BooleanField(required=False, label='Rezept veröffentlichen')
  
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation', 'work_time', 'reviewed')

IngredientFormset = modelformset_factory(Ingredient, form=CreateIngredientForm)
