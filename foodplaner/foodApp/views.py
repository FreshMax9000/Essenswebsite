from django.shortcuts import render
from django.views import generic

from . import models
from .models import Recipe, Foodplan
from users.models import Profile

def home(request):
    return render(request, 'foodApp/home.html')

class RecipesListView(generic.ListView):
    model = Recipe
    ordering = ['title']


class RecipesDetailView(generic.DetailView):
    model = Recipe

class MyProfil(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.order_by('title')
    template_name = "foodApp/myprofil.html"


class Agenda(generic.ListView):
    model = Foodplan
    queryset = Foodplan.objects.order_by('title')
    template_name = "foodApp/agenda.html"

class Shopping(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.order_by('title')
    template_name = "foodApp/shopping.html"
