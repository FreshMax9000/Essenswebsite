from django.db import transaction
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from . import models


def home(request):
    return render(request, 'foodApp/home.html')


class RecipesListView(generic.ListView):
    model = models.Recipe
    ordering = ['title']
    template_name = '.\\foodApp\\recipe_list.html'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('q', '')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return models.Recipe.objects.filter(title__icontains=self.search)


class RecipesDetailView(generic.DetailView):
    model = models.Recipe


class MyProfil(generic.ListView):
    context_object_name = 'myrecipes'
    queryset = models.Recipe.objects.order_by('title')
    template_name = "foodApp/myprofil.html"

    def get_context_data(self, **kwargs):
        context = super(MyProfil, self).get_context_data(**kwargs)
        context['myfoodplans'] = models.Foodplan.objects.order_by('user')
        return context


class Agenda(generic.DetailView):
    model = models.Foodplan
    template_name = "foodApp/agenda.html"


class Shopping(generic.ListView):
    model = models.Recipe
    queryset = models.Recipe.objects.order_by('title')
    template_name = "foodApp/shopping.html"


class CreateRecipeView(LoginRequiredMixin, generic.CreateView):
    model = models.Recipe
    fields = ['title', 'description', 'preparation', 'work_time', 'ingredients']

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
