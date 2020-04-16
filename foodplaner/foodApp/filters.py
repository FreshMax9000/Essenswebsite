"""
    This modul uses django-filter.
    Django-filter provides a simple way to filter down a queryset based on parameters a user provides.
    Guide: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
"""
import django_filters
from django import forms
from .models import Recipe
from .models import Grocerie

class FoodplanFilter(django_filters.FilterSet): #TODO:additional filters?
    """
        desc:
            - selcet attributes from Recipe to generate a filterd recipe list for Foodplan
    """
    #title = django_filters.CharFilter(lookup_expr='icontains',label="Titel enthält:")
    work_time = django_filters.NumberFilter(lookup_expr='lte', label="Maximal benötigte Zeit:")
    avg_rating = django_filters.NumberFilter(lookup_expr='gte', label="Mindest Bewertung:")
    #difficulty = django_filters.ModelMultipleChoiceFilter(queryset=['Easy','Medium,'Hard'], widget=forms.CheckboxSelectMultiple,label="Schwierigkeit:")
    ingredients = django_filters.ModelMultipleChoiceFilter(queryset=Grocerie.objects.all(), exclude=True, widget=forms.CheckboxSelectMultiple, label="Zutaten ausschließen:")

    class Meta:
        model = Recipe
        fields = ['work_time', 'avg_rating', 'ingredients']
