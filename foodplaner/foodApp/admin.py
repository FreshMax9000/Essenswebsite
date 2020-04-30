from django.contrib import admin

from . import models

admin.site.register(models.Commentary)
admin.site.register(models.Grocery)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
admin.site.register(models.Foodplan_Recipe)
admin.site.register(models.Foodplan)
