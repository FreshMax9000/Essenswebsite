from django.core.management import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group

from foodApp import models
from users.models import Profile

GROUPS_PERMISSIONS = {
    'default': {
        models.Commentary: ['add', 'view'],
        models.Grocery: ['add', 'view'],
        models.Foodplan: ['add', 'change', 'delete', 'view'],
        models.Foodplan_Recipe: ['add', 'change', 'delete', 'view'],
        models.Ingredient: ['add', 'view'],
        models.Recipe: ['add', 'change', 'view'],
        Profile: ['add', 'view'],
    },
    'pro_user': {
        models.Commentary: ['add', 'change', 'delete', 'view'],
        models.Grocery: ['add', 'change', 'delete', 'view'],
        models.Foodplan: ['add', 'change', 'delete', 'view'],
        models.Foodplan_Recipe: ['add', 'change', 'delete', 'view'],
        models.Ingredient: ['add', 'change', 'delete', 'view'],
        models.Recipe: ['add', 'change', 'delete', 'view', 'can_review'],
        Profile: ['add', 'change', 'delete', 'view'],
    },
}

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):
        # Loop groups
        for group_name in GROUPS_PERMISSIONS:

            # Get or create group
            group, created = Group.objects.get_or_create(name=group_name)
            
            #clear all and add new permissions
            if not created:
                group.permissions.clear()
            
            # Loop models in group
            for model_cls in GROUPS_PERMISSIONS[group_name]:

                # Loop permissions in group/model
                for perm_index, perm_name in \
                        enumerate(GROUPS_PERMISSIONS[group_name][model_cls]):

                    # Generate permission name as Django would generate it
                    codename = perm_name + "_" + model_cls._meta.model_name

                    try:
                        # Find permission object and add to group
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write("Adding "
                                          + codename
                                          + " to group "
                                          + group.__str__())
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
        