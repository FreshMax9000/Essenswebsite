from datetime import date
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Grocery(models.Model):
    name = models.CharField(max_length=30)
    unit = models.CharField(max_length=15, default="")

    def __str__(self):
        return f"{self.name} [{self.unit}]"


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, default="")
    preparation = models.TextField(default="")
    work_time = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0)
    difficulty = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Grocery, through='Ingredient', through_fields=('recipe', 'grocery'))
    reviewed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='recipe_images')

    def save(self, **kwargs):
        try:
            super(Recipe, self).save(**kwargs)

            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except ValueError:
            return

    def __str__(self):
        return self.title
        
    class Meta:
        permissions = (('can_review', 'Can Review Recipe'),)


class Ingredient(models.Model):
    quantity = models.FloatField(default=0)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    grocery = models.ForeignKey(Grocery, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} | {self.grocery}"


class Commentary(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(default="")
    rating = models.IntegerField(default=0)
    date = models.DateField(default=date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"Commentary {self.title} | {self.pk}"

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
