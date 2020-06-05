"""
This modul uses django-filter.

Django-filter provides a simple way to filter down a queryset based on parameters a user provides.
Guide: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
"""
import django_filters
from django import forms
from .models import Recipe
from .models import Grocery

class FoodplanFilter(django_filters.FilterSet):
    """
        desc:
            - selcet attributes from Recipe to generate a filterd recipe list for Foodplan
    """
    work_time = django_filters.NumberFilter(lookup_expr='lte', label="Maximal benötigte Zeit:")
    avg_rating = django_filters.NumberFilter(lookup_expr='gte', widget=forms.HiddenInput, label="Mindest Bewertung:")
    difficulty_choices = {(1, 'Einfach'), (2, 'Mittel'), (3, 'Schwer')}
    difficulty = django_filters.ChoiceFilter(choices=difficulty_choices, label='Schwierigkeit:')
    ingredients = django_filters.ModelMultipleChoiceFilter(queryset=Grocery.objects.all(), exclude=True, widget=forms.CheckboxSelectMultiple, label="Zutaten ausschließen")

    class Meta:
        model = Recipe
        fields = ['work_time', 'avg_rating', 'difficulty', 'ingredients']
