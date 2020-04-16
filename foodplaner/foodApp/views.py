from datetime import date
from datetime import timedelta
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Recipe
from .models import Foodplan
from .models import Foodplan_Recipe
from .filters import FoodplanFilter
from .forms import FoodplanForm
def home(request):
    return render(request, 'foodApp/home.html')

class RecipesListView(generic.ListView):
    model = Recipe
    ordering = ['title']


class RecipesDetailView(generic.DetailView):
    model = Recipe


@login_required
def foodplan(request):
    """
        desc:
            - generate Random Foodplan
            - generate complete Foodplan (for every day) or only single days
            - if User has no Foodplan object --> create new one
            - Recipes filtered in class filters.FoodplanFilter
            - no recipes cause (of filters) --> warning message
    """
    # filter list of Recipes
    foodplan_filter = FoodplanFilter(request.POST, queryset=Recipe.objects.all())
    recipe_list = foodplan_filter.qs
    # select last (temporary) Foodplan of user
    foodplan_object = Foodplan.objects.filter(user=request.user).last()

    # create new foodplan if not existing
    if foodplan_object is None:
        messages.info(request, f'Erzeuge Essenplan!')
        new_foodplan = Foodplan(user=request.user)
        new_foodplan.save()
        foodplan_object = new_foodplan

    if request.method == 'POST':
        form = FoodplanForm(request.POST)
        if 'reload' in request.POST:
            reload_recipe(request, foodplan_object, recipe_list)

        if 'delete' in request.POST:
            # select recipe to remove it from Foodplan
            removed_recipe = Recipe.objects.filter(id=request.POST.get('delete')).first()
            # remove recipe from Foodplan
            foodplan_object.recipes.remove(removed_recipe)

        # Save Foodplan (last foodplan only for temporary use!)
        # TODO: ignore last foodplan in other functions
        if 'save' in request.POST:
            messages.success(request, f'Essenplan gespeichert!')
            new_foodplan = foodplan_object
            new_foodplan.pk = None
            new_foodplan.save()
            return redirect('foodApp:home')

        if 'generate' in request.POST:
            days = int(request.POST.get('days'))
            generate_foodplan(request, foodplan_object, recipe_list, days)

    else:
        days = 5 # default value
        form = FoodplanForm()
        generate_foodplan(request, foodplan_object, recipe_list, days)

    # parameter list for the template
    context = {
        'filter': foodplan_filter,
        'form': form,
        'object_list': Foodplan_Recipe.objects.filter(foodplan=foodplan_object).order_by('date'),
    }
    return render(request, "foodApp/foodplan.html", context)

def reload_recipe(request, foodplan_object, recipe_list):
    # select recipe to remove it from Foodplan
    removed_recipe = Recipe.objects.filter(id=request.POST.get('reload')).first()
    temp_date = Foodplan_Recipe.objects.filter(foodplan=foodplan_object).filter(recipe=removed_recipe).last().date

    # filter the remaining recipes
    recipe_list = recipe_list.exclude(id=removed_recipe.id)
    for foodplan_recipe in foodplan_object.recipes.all():
        recipe_list = recipe_list.exclude(id=foodplan_recipe.id)

    # check if query_set is empty
    if recipe_list.first() is not None:
        # remove recipe from Foodplan
        foodplan_object.recipes.remove(removed_recipe)
        recipe_list = generate_recipe(request, foodplan_object, recipe_list, temp_date)
    else:
        messages.warning(request, f'Keine Rezepte vorhanden! Filter anpassen!')

def generate_foodplan(request, foodplan_object, recipe_list, days):
    # check if query_set is too short
    if len(recipe_list) >= days: #TODO replace 2 with number of days
        # clear and generate foodplan
        foodplan_object.recipes.clear()
        for count in range(days):
            recipe_list = generate_recipe(request, foodplan_object, recipe_list, date.today() + timedelta(days=count))
    else:
        messages.warning(request, f'Keine Rezepte vorhanden! Filter anpassen!')

def generate_recipe(request, foodplan_object, recipe_list, temp_date):
    """
        desc:
            - select(randomly) and add new recipe to foodplan
        para:
            - recipe_list --> select one recipe from the list of recipes
            - foodplan --> foodplan instance of current user
            - temp_date --> set Day of foodplan
        ret:
            - return recipe_list exclude the selected recipe
    """
    random_recipes = recipe_list.order_by('?').first() #@test: generate 2 recipe
    foodplan_object.recipes.add(random_recipes)
    save_date = Foodplan_Recipe.objects.filter(foodplan=foodplan_object).filter(recipe=random_recipes).last()
    save_date.date = temp_date
    save_date.save()
    return recipe_list.exclude(id=random_recipes.id)
