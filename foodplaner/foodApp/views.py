from datetime import date
from datetime import timedelta

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Recipe
from .models import Ingredient
from .models import Grocery
from .models import Foodplan
from .models import Foodplan_Recipe
from .filters import FoodplanFilter
from .forms import FoodplanForm
from .forms import IngredientFormset
from .forms import RecipeForm
from .forms import CreateGroceryForm


def home(request):
    return render(request, 'foodApp/home.html')

def home_design2(request):
    return render(request, 'foodApp/home_design2.html')

def get_recipe_object():
    """
        desc:
            - view only reviewed Recipes
            - use this function instead of "Recipe.objects"
    """
    return Recipe.objects.filter(reviewed=True)


class RecipesListView(generic.ListView):
    model = Recipe
    ordering = ['title']
    template_name = "foodApp/recipe_list.html"
    paginate_by = 10

    def get_queryset(self):
        return get_recipe_object().filter(title__icontains=self.request.GET.get('q', '')).order_by('title')


class ReviewRecipesListView(PermissionRequiredMixin, generic.ListView):
    model = Recipe
    ordering = ['title']
    template_name = "foodApp/recipe_list.html"
    paginate_by = 10
    permission_required = 'foodApp.change_recipe'

    def get_queryset(self):
        recipe_object = Recipe.objects.filter(reviewed=False)
        return recipe_object.filter(title__icontains=self.request.GET.get('q', '')).order_by('title')


class RecipesDetailView(UserPassesTestMixin, generic.DetailView):
    model = Recipe

    def test_func(self):
        is_valid = False
        if self.request.user.has_perm('foodApp.change_recipe'):
            is_valid = True
        else:
            is_valid = self.get_object() in get_recipe_object()
        return is_valid


class MyProfil(LoginRequiredMixin, generic.ListView):
    template_name = "foodApp/myprofil.html"

    def get_queryset(self):
        self.context_object_name = 'myrecipes'
        queryset = get_recipe_object().filter(author=self.request.user).order_by('title')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyProfil, self).get_context_data(**kwargs)
        # exclude last foodplan --> only for temporary use
        foodplan_object = Foodplan.objects.filter(user=self.request.user)
        if foodplan_object.last() is not None:
            context['myfoodplans'] = foodplan_object.exclude(id=foodplan_object.last().id)
        return context


class Agenda(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Foodplan
    template_name = "foodApp/agenda.html"

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, **kwargs):
        context = super(Agenda, self).get_context_data(**kwargs)
        context['object_list'] = Foodplan_Recipe.objects.filter(foodplan_id=self.kwargs.get('pk')).order_by('date')
        return context


class Shopping(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Foodplan
    template_name = "foodApp/shopping.html"

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, **kwargs):
        context = super(Shopping, self).get_context_data(**kwargs)
        context['object_list'] = self.get_ingredient_list(Foodplan.objects.get(id=self.kwargs.get('pk')).recipes)
        return context

    def get_ingredient_list(self, recipe_list):
        """
            desc:
                - creates a dict from the given recipes and sums up all ingredients
            para:
                - recipe_list - list of recipes to be summed up
            ret:
                - dict_ingredient_as_string - returns a dict of strings of summed ingredients
        """
        dict_ingredient_as_string = {}
        dict_ingredient_value = {}
        for recipe in recipe_list.all():
            for ingredient in Ingredient.objects.filter(recipe_id=recipe.id):
                # If ingredient already exists in dictionary, sum the quantity
                # If not, ad the ingredient to Dictionary
                quantity = ingredient.quantity
                key = ingredient.grocery.name
                if key in dict_ingredient_value:
                    quantity += dict_ingredient_value.get(key)[0]
                    dict_ingredient_value[key] = (quantity, ingredient.grocery.unit)
                else:
                    dict_ingredient_value[key] = (quantity, ingredient.grocery.unit)

        for key in sorted(dict_ingredient_value.keys()):
            quantity = dict_ingredient_value.get(key)[0]
            unit = dict_ingredient_value.get(key)[1]
            if dict_ingredient_value.get(key)[0] >= 1000:
                quantity = quantity/1000
                if dict_ingredient_value.get(key)[1] == 'ml':
                    unit = 'l'
                elif dict_ingredient_value.get(key)[1] == 'g':
                    unit = 'kg'
            dict_ingredient_as_string[key] = str(quantity) + " " + unit

        return dict_ingredient_as_string


class CreateRecipeView(PermissionRequiredMixin, generic.CreateView):
    model = Recipe
    form_class = RecipeForm
    success_url = reverse_lazy('foodApp:home')
    permission_required = 'foodApp.add_recipe'

    def get_context_data(self, **kwargs):
        if self.request.method == 'GET':
            recipe_form = RecipeForm(self.request.GET or None)
            formset = IngredientFormset(queryset=Ingredient.objects.none())
        elif self.request.method == 'POST':
            recipe_form = RecipeForm(self.request.POST)
            formset = IngredientFormset(self.request.POST)

        context = super(CreateRecipeView, self).get_context_data(**kwargs)
        context['formset'] = formset
        context['recipe_form'] = recipe_form
        return context

    def form_valid(self, form):
        if self.request.method == 'GET':
            formset = IngredientFormset(queryset=Ingredient.objects.none())
        elif self.request.method == 'POST':
            formset = IngredientFormset(self.request.POST)

        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()
            
        for ingredient_form in formset:
            # skip if a form is invalid
            try:
                ingredient = ingredient_form.save(commit=False)
            except ValueError:
                print('ValueError ')
            else:
                if ingredient_form.cleaned_data:
                    ingredient.recipe = recipe
                    ingredient.save()
        return super().form_valid(form)


class UpdateRecipeView(PermissionRequiredMixin, generic.UpdateView):
    model = Recipe

    success_url = reverse_lazy('foodApp:home')
    permission_required = 'foodApp.change_recipe'
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        if self.request.method == 'GET':
            recipe_form = RecipeForm(self.request.GET)

            recipe = Recipe.objects.get(id=self.kwargs['pk'])
            recipe_form = RecipeForm(initial={
                'title': recipe.title,
                'description': recipe.description,
                'preparation': recipe.preparation,
                'work_time': recipe.work_time,
                'reviewed': recipe.reviewed,
            })

            formset = IngredientFormset(queryset=Ingredient.objects.filter(recipe_id=self.kwargs['pk']))
        elif self.request.method == 'POST':
            recipe_form = RecipeForm(self.request.POST)
            formset = IngredientFormset(self.request.POST)

        context = super(UpdateRecipeView, self).get_context_data(**kwargs)
        context['recipe_form'] = recipe_form
        context['formset'] = formset
        return context

    def form_valid(self, form):
        if self.request.method == 'POST':
            formset = IngredientFormset(self.request.POST)

            form.save()
            count_saved_forms = 0
            for ingredient_form in formset:
                # skip if a form is invalid
                try:
                    ingredient = ingredient_form.save(commit=False)
                except ValueError:
                    print('ValueError ')
                else:
                    if ingredient_form.cleaned_data:
                        count_saved_forms += 1
                        ingredient.recipe = Recipe.objects.get(id=self.kwargs['pk'])
                        ingredient.save()

            # necessary because the updateView didn't delete any ingredients
            # ingredients only got updated or added
            # -> delete ingredients that had not been updated
            ingredient_list = Ingredient.objects.filter(recipe_id=self.kwargs['pk'])[count_saved_forms:]
            for element in ingredient_list:
                element.delete()
        return super().form_valid(form)


class DeleteRecipeView(PermissionRequiredMixin, generic.DeleteView):
    model = Recipe
    success_url = reverse_lazy('foodApp:home')
    permission_required = 'foodApp.delete_recipe'


class CreateGroceryView(PermissionRequiredMixin, generic.CreateView):
    model = Grocery
    form_class = CreateGroceryForm
    success_url = reverse_lazy('foodApp:home')
    permission_required = 'foodApp.add_grocery'


class UpdateGroceryView(PermissionRequiredMixin, generic.UpdateView):
    model = Grocery
    form_class = CreateGroceryForm
    success_url = reverse_lazy('foodApp:home')
    permission_required = 'foodApp.change_grocery'


class DeleteGroceryView(PermissionRequiredMixin, generic.DeleteView):
    model = Grocery
    success_url = reverse_lazy('foodApp:home')
    permission_required = 'foodApp.delete_recipe'


class DeleteFoodplanView(PermissionRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Foodplan
    success_url = reverse_lazy('foodApp:myprofil')
    permission_required = 'foodApp.delete_foodplan'

    def test_func(self):
        return self.request.user == self.get_object().user


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
    foodplan_filter = FoodplanFilter(request.POST, queryset=get_recipe_object())
    recipe_list = foodplan_filter.qs
    # select last (temporary) Foodplan of user
    foodplan_object = Foodplan.objects.filter(user=request.user).last()

    # create new foodplan if not existing
    if foodplan_object is None:
        new_foodplan = Foodplan(user=request.user)
        new_foodplan.save()
        foodplan_object = new_foodplan

    if request.method == 'POST':
        form = FoodplanForm(request.POST)
        if 'reload' in request.POST:
            reload_recipe(request, foodplan_object, recipe_list)

        if 'delete' in request.POST:
            # select recipe to remove it from Foodplan
            removed_recipe = get_recipe_object().filter(id=request.POST.get('delete')).first()
            # remove recipe from Foodplan
            foodplan_object.recipes.remove(removed_recipe)

        # Save Foodplan (last foodplan only for temporary use!)
        if 'save' in request.POST:
            messages.success(request, f'Essenplan gespeichert!')
            new_foodplan = Foodplan(user=request.user)
            new_foodplan.save()
            return redirect('foodApp:agenda', foodplan_object.id)

        if 'generate' in request.POST:
            days = int(request.POST.get('days'))
            selected_daytime = request.POST.get('select_daytime')
            generate_foodplan(request, foodplan_object, recipe_list, days, selected_daytime)

    else:
        days = 5 # default value
        selected_daytime = '1' # default
        form = FoodplanForm()
        generate_foodplan(request, foodplan_object, recipe_list, days, selected_daytime)

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
    removed_recipe = get_recipe_object().get(id=request.POST.get('reload'))
    temp_date = Foodplan_Recipe.objects.filter(foodplan=foodplan_object).get(recipe=removed_recipe).date
    daytime = Foodplan_Recipe.objects.filter(foodplan=foodplan_object).get(recipe=removed_recipe).daytime

    # filter the remaining recipes
    recipe_list = recipe_list.exclude(id=removed_recipe.id)
    for foodplan_recipe in foodplan_object.recipes.all():
        recipe_list = recipe_list.exclude(id=foodplan_recipe.id)

    # check if query_set is empty
    if recipe_list.first() is not None:
        # remove recipe from Foodplan
        foodplan_object.recipes.remove(removed_recipe)
        recipe_list = generate_recipe(request, foodplan_object, recipe_list, temp_date, daytime)
    else:
        messages.warning(request, f'Keine Rezepte vorhanden! Filter anpassen!')


def generate_foodplan(request, foodplan_object, recipe_list, days, selected_daytime):
    """
        desc:
            - clear foodplan
            - choose number of days random recipes from recipe_list
            - add choosen recipes to foodplan
            - if recipes < days --> warning
    """
    if selected_daytime == '1':
        days = days * 2
        daytime = True
    elif selected_daytime == '2':
        daytime = True
    else:
        daytime = False
    # check if query_set is too short
    if len(recipe_list) >= days:
        # clear and generate foodplan
        foodplan_object.recipes.clear()
        temp_date = date.today()
        for count in range(days):
            recipe_list = generate_recipe(request, foodplan_object, recipe_list, temp_date, daytime)
            if selected_daytime == '1':
                daytime = not daytime
                if daytime:
                    temp_date += timedelta(days=1)
            else:
                temp_date += timedelta(days=1)
    else:
        messages.warning(request, f'Keine Rezepte vorhanden! Filter anpassen!')


def generate_recipe(request, foodplan_object, recipe_list, temp_date, daytime):
    """
        desc:
            - select(randomly) and add new recipe to foodplan
        para:
            - recipe_list --> select one recipe from the list of recipes
            - foodplan --> foodplan instance of current user
            - temp_date --> set Day of foodplan
            - daytime --> True = lunch, False = dinner
        ret:
            - return recipe_list exclude the selected recipe
    """
    random_recipes = recipe_list.order_by('?').first()
    foodplan_object.recipes.add(random_recipes)
    save_date = Foodplan_Recipe.objects.filter(foodplan=foodplan_object).get(recipe=random_recipes)
    save_date.date = temp_date
    save_date.daytime = daytime
    save_date.save()
    return recipe_list.exclude(id=random_recipes.id)
