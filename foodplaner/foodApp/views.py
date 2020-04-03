from django.shortcuts import render
from django.views import generic

from .models import Recipes
from users.models import Profile

def home(request):
    return render(request, 'foodApp/home.html')

class RecipesListView(generic.ListView):
    model = Recipes
    ordering = ['title']


class RecipesDetailView(generic.DetailView):
    model = Recipes

def MyProfil(request):
    Recipe = [Recipes.title]
    return render(request, 'foodApp/myProfil.html', {'Recip' : Recipe})


def Wochenplan(request):
    return render(request, 'foodApp/Wochenplan.html')
