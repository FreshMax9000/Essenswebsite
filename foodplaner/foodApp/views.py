from django.shortcuts import render
from django.views import generic

from .models import Recipes

def index(request):
    return render(request, 'foodApp/index.html')

class RecipesView(generic.DetailView):
    model = Recipes
    template_name = 'foodapp/recipes.html'
