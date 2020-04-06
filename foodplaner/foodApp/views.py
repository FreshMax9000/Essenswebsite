from django.shortcuts import render
from django.views import generic

from . import models
from .models import Recipe
from users.models import Profile

def home(request):
    return render(request, 'foodApp/home.html')

class RecipesListView(generic.ListView):
    model = models.Recipe
    ordering = ['title']


class RecipesDetailView(generic.DetailView):
    model = models.Recipe

def MyProfil(request):
    Recipes = [Recipe.title]
    return render(request, 'foodApp/myProfil.html', {'Recip' : Recipes})


def Wochenplan(request):
    return render(request, 'foodApp/Wochenplan.html')
