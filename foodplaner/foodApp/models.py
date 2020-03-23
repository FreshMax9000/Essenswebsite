from django.db import models


class Ingredients(models.Model):
    name = models.CharField(max_length=200)

class Recipes(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
