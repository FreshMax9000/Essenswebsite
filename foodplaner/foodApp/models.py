from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Grocery(models.Model):
    name = models.CharField(max_length=30)
    unit = models.CharField(max_length=15, default="")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, default="")
    preparation = models.TextField(default="")
    work_time = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0) #@TODO: durchschnitt berechnen aus allen kommentaren, neuberechnung wenn neuer kommentar/ kommnetar änderung/ löschung
    # difficulty
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Grocery, through='Ingredient', through_fields=('recipe', 'grocery'))
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
# wenn man das hinzugefügte Retept anzeigen will:
#    def get_absolute_url(self):
#        return reverse('recipesDetail', kwargs={'pk': self.pk})


class Ingredient(models.Model):
    quantity = models.FloatField(default=0)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    grocery = models.ForeignKey(Grocery, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} | {self.grocery}"


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
    date = models.DateField(default=date.today)
    daytime = models.BooleanField(default=True) # True = lunch | False = dinner
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    foodplan = models.ForeignKey(Foodplan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.foodplan} | Day {self.date}"
