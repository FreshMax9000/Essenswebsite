from django.db import transaction
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from extra_views import CreateWithInlinesView
from extra_views import InlineFormSet

from . import forms
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

'''
class CreateRecipeView(LoginRequiredMixin, generic.CreateView):
    model = models.Recipe
    context_object_name = 'recipesDetail'
    # fields = ['title', 'description', 'preparation', 'work_time', 'ingredients']
    form_class = forms.CreateRecipeForm
    template_name = 'foodApp/recipe_form.html'
    success_url = '/'  # home

    def get_context_data(self, **kwargs):
        data = super(CreateRecipeView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['ingredients'] = forms.CreateIngredientForm(self.request.POST)
        else:
            data['ingredients'] = forms.CreateIngredientForm()
        return data

    #def form_valid(self, form):
    #    form.instance.author = self.request.user
    #    return super().form_valid(form)

    def form_valid(self, form):
        context = self.get_context_data()
        ingredients = context['ingredients']
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            if ingredients.is_valid():
                ingredients.instance = self.object
                ingredients.save()
        return super(CreateRecipeView, self).form_valid(form)
'''
class CreateIngredientView(InlineFormSet, generic.CreateView):
    model = models.Ingredient
    fields = ['grocerie', 'quantity']


class CreateRecipeView(LoginRequiredMixin, generic.CreateView):
    model = models.Recipe
    queryset = Recipe.objects.all()
    fields = ['title', 'description', 'preparation', 'work_time', 'ingredients']
    inlines = [CreateIngredientView, ]

    #def get_context_data(self, **kwargs):
    #    context = super(CreateRecipeView, self).get_context_data(**kwargs)
    #    context['ingredients'] = models.Ingredient.objects.all()
    #    # And so on for more models
    #    return context

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
