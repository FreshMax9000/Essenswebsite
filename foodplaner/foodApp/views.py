from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User

from .models import Recipe

def home(request):
    return render(request, 'foodApp/home.html')

class foodplanListView(generic.ListView):
    model = Recipe
    template_name = "foodapp/foodplan.html"
    queryset = Recipe.objects.order_by('?')


class RecipesListView(generic.ListView):
    model = Recipe
    ordering = ['title']


class RecipesDetailView(generic.DetailView):
    model = Recipe
