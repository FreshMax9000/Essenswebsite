from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

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


class CreateRecipeView(LoginRequiredMixin, generic.CreateView):
    model = models.Recipe
    fields = ['title', 'description', 'preparation', 'work_time', 'ingredients']

    success_url = '/'  # home

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateRecipeView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = models.Recipe
    fields = ['title', 'description', 'preparation', 'work_time', 'ingredients']

    success_url = '/'  # home

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # A recipe can only get updated by the user that created it -> change later to admins
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


class CreateGroceryView(LoginRequiredMixin, generic.CreateView):
    model = models.Grocerie
    fields = ['name', 'unit']

    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)


class DeleteRecipeView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = models.Recipe
    success_url = '/'

    # A recipe can only get deleted by the user that created it -> change later to admins
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author
