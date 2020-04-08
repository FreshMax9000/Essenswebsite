from django.shortcuts import render
from django.views import generic

from . import models
from .models import Recipe


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


class CreateRecipeView(generic.CreateView):
    model = models.Recipe
    fields = ['title', 'description', 'preparation', 'work_time', 'ingredients']

    success_url = '/'  # home

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CreateGroceryView(generic.CreateView):
    model = models.Grocerie
    fields = ['name', 'unit']

    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)
