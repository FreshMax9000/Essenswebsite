"""
In this module functions are defined that catch signals which are raised somewhere else.
"""
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Object of type profile gets generated with default user rights and saved to the database.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Profile gets saved to database.
    """
    instance.profile.save()
