# Generated by Django 3.0.4 on 2020-04-01 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodApp', '0004_auto_20200324_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredients',
            name='unit',
            field=models.CharField(default='', max_length=100),
        ),
    ]
