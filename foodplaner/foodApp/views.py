from django.shortcuts import render
from django.views import generic
from users.models import Profile
from . import models
from .models import Recipe

def home(request):
    return render(request, 'foodApp/home.html')

class RecipesListView(generic.ListView):
    model = models.Recipe
    paginate_by = 20
    ordering = ['title']


class SearchRecipesView(generic.ListView):
    model = models.Recipe
    ordering = ['title']
    template_name = '.\\foodApp\\search_recipe.html'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('q', '')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return models.Recipe.objects.filter(title__icontains=self.search)


class RecipesDetailView(generic.DetailView):
    model = models.Recipe

def MyProfil(request):
    Recipes = [Recipe.title]
    return render(request, 'foodApp/myProfil.html', {'Recipe' : Recipes})


def Wochenplan(request):
    return render(request, 'foodApp/Wochenplan.html')

