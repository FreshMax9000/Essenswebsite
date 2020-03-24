from django.db import models


class Ingredients(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Recipes(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200,default="")
    preparation = models.TextField(default="")
    work_time = models.IntegerField(default=0)
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    #author = user.
    
    def __str__(self):
        return self.title
    
