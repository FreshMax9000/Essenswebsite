from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Recipe
from .models import Foodplan

def home(request):
    return render(request, 'foodApp/home.html')

class RecipesListView(generic.ListView):
    model = Recipe
    ordering = ['title']


class RecipesDetailView(generic.DetailView):
    model = Recipe

@login_required
def foodplan(request):
    recipe_objects = Recipe.objects.filter(avg_rating__gt=3) #filter this list for an filterd result .all() for unfilterd
    foodplan = Foodplan.objects.filter(user=request.user).first()
    if foodplan is None:
        messages.info(request, f'Erzeuge Essenplan!')
        new_foodplan = Foodplan(user=request.user)
        new_foodplan.save()
        foodplan = new_foodplan

    if request.method == 'POST' and 'submit' not in request.POST:
        if 'reload' in request.POST:
            # select recipe to remove it from Foodplan
            removed_recipe = Recipe.objects.filter(id = request.POST.get('reload')).first()

            # filter the remaining recipes
            recipe_objects=recipe_objects.exclude(id = removed_recipe.id)
            for foodplan_recipe in foodplan.recipes.all():
                recipe_objects=recipe_objects.exclude(id = foodplan_recipe.id)

            # check if query_set is empty
            if recipe_objects.first() is not None: 
                # remove recipe from Foodplan
                foodplan.recipes.remove(removed_recipe)
                # select and add new recipe to foodplan
                random_recipes =recipe_objects.order_by('?').first()
                foodplan.recipes.add(random_recipes)
            else:
                messages.info(request, f'Keine Rezepte vorhanden!')
            # get all recipes in foodplan
            object_list = foodplan.recipes.all()
    else:
        # clear and generate foodplan 
        foodplan.recipes.clear()
        object_list = recipe_objects.order_by('?')[:2] #@test: generate 2 recipe 
        foodplan.recipes.add(*object_list)

    # context given to the template
    context={
        'object_list': object_list
    }
    return render(request, "foodApp/foodplan.html", context)