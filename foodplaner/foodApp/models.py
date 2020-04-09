from django.db import models
from django.contrib.auth.models import User


class Grocerie(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100,default="")

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200,default="")
    preparation = models.TextField(default="")
    work_time = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0) #@TODO: durchschnitt berechnen aus allen kommentaren, neuberechnung wenn neuer kommentar/ kommnetar änderung/ löschung
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Grocerie, through='Ingredient', through_fields=('recipe', 'grocerie'))
    
    def __str__(self):
        return self.title
    

class Ingredient(models.Model):
    quantity = models.FloatField(default=0)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    grocerie = models.ForeignKey(Grocerie, on_delete=models.CASCADE)


class Commentary(models.Model):
    text = models.TextField(default="")
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
class Foodplan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe, through='Foodplan_Recipe')
    
    def __str__(self):
        return f"{self.user}'s Foodplan"

    
class Foodplan_Recipe(models.Model):
    #date = models.TimeField();#12Uhr mittagesssen #18uhr abendessen
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    foodplan = models.ForeignKey(Foodplan, on_delete=models.CASCADE)
