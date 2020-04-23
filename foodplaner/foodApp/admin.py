"""
Register pages for admins to edit models in automatically generated admin interface.
"""
from django.contrib import admin

from . import models

admin.site.register(models.Grocerie)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
admin.site.register(models.Foodplan_Recipe)
admin.site.register(models.Foodplan)

#Admin Funktion mit /admin in den admin bereich