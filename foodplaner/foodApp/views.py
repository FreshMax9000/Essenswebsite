from datetime import date
from datetime import timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Recipe
from .models import Ingredient
from .models import Grocerie
from .models import Foodplan
from .models import Foodplan_Recipe
from .filters import FoodplanFilter
from .forms import FoodplanForm
from .forms import IngredientFormset
from .forms import CreateRecipeForm
from .forms import CreateGroceryForm


def home(request):
    return render(request, 'foodApp/home.html')


class RecipesListView(generic.ListView):
    model = Recipe
    ordering = ['title']
    template_name = '.\\foodApp\\recipe_list.html'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('q', '')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Recipe.objects.filter(title__icontains=self.search)


class RecipesDetailView(generic.DetailView):
    model = Recipe


class MyProfil(LoginRequiredMixin, generic.ListView):
    template_name = "foodApp/myprofil.html"

    def get_queryset(self):
        self.context_object_name = 'myrecipes'
        queryset = Recipe.objects.filter(author=self.request.user).order_by('title')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyProfil, self).get_context_data(**kwargs)
        # exclude last foodplan --> only for temporary use
        foodplan_object = Foodplan.objects.filter(user=self.request.user)
        if foodplan_object.last() is not None:
            context['myfoodplans'] = foodplan_object.exclude(id=foodplan_object.last().id)
        return context


class Agenda(LoginRequiredMixin, generic.DetailView):
    model = Foodplan
    template_name = "foodApp/agenda.html"

    def get_context_data(self, **kwargs):
        context = super(Agenda, self).get_context_data(**kwargs)
        context['object_list'] = Foodplan_Recipe.objects.filter(foodplan_id=self.kwargs.get('pk'))
        return context

class Shopping(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = "foodApp/shopping.html"

    def get_context_data(self, **kwargs):
        context = super(Shopping, self).get_context_data(**kwargs)
        context['object_list'] = self.get_ingrediant_list(Foodplan.objects.get(id=self.kwargs.get('pk')).recipes)
        return context

    def get_ingrediant_list(self, recipe_list):
        """
            desc:
                - creates a dict from the given recipes and sums up all ingredients
            para:
                - recipe_list - list of recipes to be summed up
            ret:
                - dict_ingrediant_as_string - returns a dict of strings of summed ingredients
        """
        dict_ingrediant_as_string = {}
        dict_ingrediant_value = {}
        for recipe in recipe_list.all():
            for ingrediant in Ingredient.objects.filter(recipe_id=recipe.id):
                # If ingrediant already exists in dictionary, sum the quantity
                # If not, ad the ingrediant to Dictionary
                quantity = ingrediant.quantity
                if ingrediant.grocerie.name in dict_ingrediant_value:
                    quantity = quantity + dict_ingrediant_value.get(ingrediant.grocerie.name)[0]
                    dict_ingrediant_value[ingrediant.grocerie.name] = (quantity, ingrediant.grocerie.unit)
                else:
                    dict_ingrediant_value[ingrediant.grocerie.name] = (quantity, ingrediant.grocerie.unit)

            for key, value in dict_ingrediant_value.items():
                dict_ingrediant_as_string[key] = str(value[0]) + str(" ") + str(value[1])

        return dict_ingrediant_as_string


@login_required
def create_recipe(request):
    template_name = 'foodApp/recipe_create.html'
    if request.method == 'GET':
        recipe_form = CreateRecipeForm(request.GET or None)
        formset = IngredientFormset(queryset=Ingredient.objects.none())
    elif request.method == 'POST':
        recipe_form = CreateRecipeForm(request.POST)
        formset = IngredientFormset(request.POST)
        if recipe_form.is_valid() and formset.is_valid():
            user = request.user
            recipe_form.instance.author = user
            if user.has_perm('foodApp.change_recipe'):
                #form.instance.reviewed = True
                pass
            recipe = recipe_form.save()
            
            for form in formset:
                ingredient = form.save(commit=False)
                ingredient.recipe = recipe
                ingredient.save()
            return redirect('foodApp:home')
    return render(request, template_name, {'recipe_form': recipe_form, 'formset': formset})


class UpdateRecipeView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Recipe
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
    model = Grocerie
    form_class = CreateGroceryForm
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)


class DeleteRecipeView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Recipe
    success_url = '/'

    # A recipe can only get deleted by the user that created it -> change later to admins
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


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
    """
        desc:
            - reload single recipe
            - remove choosen recipe(id saved in request.Post)
            - choose random recipe from recipe_list
            - add recipe too foodplan with origin date
            - if recipe_list only removed recipe --> do noting + warning
    """
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
    """
        desc:
            - clear foodplan
            - choose number of days random recipes from recipe_list
            - add choosen recipes to foodplan
            - if recipes < days --> warning
    """
    # check if query_set is too short
    if len(recipe_list) >= days:
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
    random_recipes = recipe_list.order_by('?').first()
    foodplan_object.recipes.add(random_recipes)
    save_date = Foodplan_Recipe.objects.filter(foodplan=foodplan_object).filter(recipe=random_recipes).last()
    save_date.date = temp_date
    save_date.save()
    return recipe_list.exclude(id=random_recipes.id)
