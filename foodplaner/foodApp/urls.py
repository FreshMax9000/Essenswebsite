"""
foodplaner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views

app_name = 'foodApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('Suche', views.RecipesListView.as_view(), name='recipesList'),
    path('Rezepte/<int:pk>/', views.RecipesDetailView.as_view(), name='recipesDetail'),
    path('Rezepte/<int:pk>/loeschen/', views.DeleteRecipeView.as_view(), name='recipesDelete'),
    path('Rezepte/<int:pk>/bearbeiten/', views.UpdateRecipeView.as_view(), name='recipesUpdate'),
    path('Rezepte/hinzufuegen/', views.CreateRecipeView.as_view(), name='addRecipe'),
    path('Zutat_hinzufuegen/', views.CreateGroceryView.as_view(), name='addGrocery'),
    path('MeinProfil/', views.MyProfil.as_view(), name='myprofil'),
    path('MeinWochenplan/<int:pk>/', views.Agenda.as_view(), name='agenda'),
    path('Einkaufsliste/<int:pk>/', views.Shopping.as_view(), name='shopping'),
    path('Essensplan/', views.foodplan, name='foodplan'),
]
