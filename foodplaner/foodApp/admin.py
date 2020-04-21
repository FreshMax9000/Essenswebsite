"""
Automatic admin interface. 
It reads metadata from the models to provide a quick, model-centric interface where trusted users can manage content. 
The admin’s recommended use is limited to an organization’s internal management tool.
"""

from django.contrib import admin

from . import models

admin.site.register(models.Grocerie)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
admin.site.register(models.Foodplan_Recipe)
admin.site.register(models.Foodplan)
