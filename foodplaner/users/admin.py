"""
Register pages for admins to edit models in automatically generated admin interface.
"""
from django.contrib import admin
from .models import Profile


admin.site.register(Profile)