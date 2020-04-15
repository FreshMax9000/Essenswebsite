from django import forms
import django_filters
from .models import Recipe
from .models import Grocerie

class FoodplanFilter(django_filters.FilterSet): #TODO:additional filters? -->Guid:https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
    #title = django_filters.CharFilter(lookup_expr='icontains',label="Titel enthält:")
    work_time = django_filters.NumberFilter(lookup_expr='lte', label="Maximal benötigte Zeit:")
    avg_rating = django_filters.NumberFilter(lookup_expr='gte', label="Mindest Bewertung:")
    #difficulty = django_filters.ModelMultipleChoiceFilter(queryset=['Easy','Medium,'Hard'], widget=forms.CheckboxSelectMultiple,label="Schwierigkeit:")
    ingredients = django_filters.ModelMultipleChoiceFilter(queryset=Grocerie.objects.all(), widget=forms.CheckboxSelectMultiple, label="Zutaten:") #TODO: Grocerie.objects.filter(reviewd=true)

    class Meta:
        model = Recipe
        fields = ['work_time', 'avg_rating', 'ingredients']
