"""
This document contains models to store persistent data.

Models are objects which internally translate the data they contain to a SQL database. Therefore models can be
treated like object but the data they contain is stored persistent and efficient in a SQL database.
For more information see https://docs.djangoproject.com/en/3.0/topics/db/models/
"""


from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
        super(Profile, self).save(**kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
