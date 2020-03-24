from django.shortcuts import render
from django.views import generic

from .models import Recipes

def home(request):
    return render(request, 'foodApp/home.html')

class RecipesListView(generic.ListView):
    model = Recipes


class RecipesDetailView(generic.DetailView):
    model = Recipes