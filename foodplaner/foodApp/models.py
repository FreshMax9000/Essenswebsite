"""
A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.

The basics:

Each model is a Python class that subclasses django.db.models.Model.
Each attribute of the model represents a database field.
With all of this, Django gives you an automatically-generated database-access API
"""

from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Grocerie(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, default="")
    preparation = models.TextField(default="")
    work_time = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0) #@TODO: durchschnitt berechnen aus allen kommentaren, neuberechnung wenn neuer kommentar/ kommnetar änderung/ löschung
    # difficulty
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Grocerie, through='Ingredient', through_fields=('recipe', 'grocerie'))
    # was_reviewed = models.BooleanField(default=True)  # muss später noch auf False gesetzt werden

    def __str__(self):
        return self.title
# wenn man das hinzugefügte Retept anzeigen will:
#    def get_absolute_url(self):
#        return reverse('recipesDetail', kwargs={'pk': self.pk})


class Ingredient(models.Model):
    quantity = models.FloatField(default=0)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    grocerie = models.ForeignKey(Grocerie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} | {self.grocerie}"


class Commentary(models.Model):
    text = models.TextField(default="")
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Foodplan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe, through='Foodplan_Recipe')

    def __str__(self):
        return f"{self.user}'s Foodplan ({self.pk})"


class Foodplan_Recipe(models.Model):
    date = models.DateField(default=date.today) #TODO: 2 Meals per day
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    foodplan = models.ForeignKey(Foodplan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.foodplan} | Day {self.date}"
