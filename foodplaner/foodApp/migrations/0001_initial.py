# Generated by Django 3.0.5 on 2020-05-04 15:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Foodplan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Grocery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('unit', models.CharField(default='', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('grocery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodApp.Grocery')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(default='', max_length=100)),
                ('preparation', models.TextField(default='')),
                ('work_time', models.IntegerField(default=0)),
                ('avg_rating', models.FloatField(default=0)),
                ('difficulty', models.IntegerField(default=0)),
                ('reviewed', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='recipe_images')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(through='foodApp.Ingredient', to='foodApp.Grocery')),
            ],
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodApp.Recipe'),
        ),
        migrations.CreateModel(
            name='Foodplan_Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('daytime', models.BooleanField(default=True)),
                ('foodplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodApp.Foodplan')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodApp.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='foodplan',
            name='recipes',
            field=models.ManyToManyField(through='foodApp.Foodplan_Recipe', to='foodApp.Recipe'),
        ),
        migrations.AddField(
            model_name='foodplan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Commentary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(default='')),
                ('rating', models.IntegerField(default=0)),
                ('date', models.DateField(default=datetime.date.today)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodApp.Recipe')),
            ],
        ),
    ]
