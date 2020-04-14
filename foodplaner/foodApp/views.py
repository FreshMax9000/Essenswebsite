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
    context_object_name = 'myrecipes'
    queryset = Recipe.objects.order_by('title')

    template_name = "foodApp/myprofil.html"

    def get_context_data(self, **kwargs):
        context = super(MyProfil, self).get_context_data(**kwargs)
        context['myfoodplans'] = Foodplan.objects.order_by('user')
        return context


class Agenda(generic.DetailView):
    model = Foodplan
    template_name = "foodApp/agenda.html"

class Shopping(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.order_by('title')
    template_name = "foodApp/shopping.html"
