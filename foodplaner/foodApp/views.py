from django.shortcuts import render
from django.views import generic

from . import models

def home(request):
    return render(request, 'foodApp/home.html')

class RecipesListView(generic.ListView):
    model = models.Recipe
    ordering = ['title']


class RecipesDetailView(generic.DetailView):
    model = models.Recipe