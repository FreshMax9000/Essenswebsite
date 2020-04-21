"""
Signal dispatcher which helps allow decoupled applications get notified when actions occur elsewhere in the framework. 
In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place. 
They’re especially useful when many pieces of code may be interested in the same events.
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
