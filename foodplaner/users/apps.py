"""
The term application describes a Python package that provides some set of features. 
Applications may be reused in various projects.
Applications include some combination of models, views, templates, template tags, static files, URLs, middleware, etc. 
They’re generally wired into projects with the INSTALLED_APPS setting and optionally with other mechanisms such as URLconfs, 
the MIDDLEWARE setting, or template inheritance.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
