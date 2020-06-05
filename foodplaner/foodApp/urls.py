"""
This document defines the link between given URLs and Python functions to generate the corresponding view.

For more information see https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""


from django.urls import path

from . import views

app_name = 'foodApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('Suche', views.RecipesListView.as_view(), name='recipesList'),
    path('Verifizieren', views.ReviewRecipesListView.as_view(), name='reviewRecipesList'),
    path('Rezept/<int:pk>/', views.RecipesDetailView.as_view(), name='recipesDetail'),
    path('Rezept/hinzufuegen/', views.CreateRecipeView.as_view(), name='addRecipe'),
    path('Rezept/<int:pk>/loeschen/', views.DeleteRecipeView.as_view(), name='recipesDelete'),
    path('Rezept/<int:pk>/bearbeiten/', views.UpdateRecipeView.as_view(), name='recipesUpdate'),
    path('Rezept/<int:pk>/Kommentare/hinzufuegen/', views.CommentaryCreateView.as_view(), name='createCommentary'),
    path('Rezept/Kommentare/<int:pk>/bearbeiten/', views.CommentaryUpdateView.as_view(), name='updateCommentary'),
    path('Rezept/Kommentare/<int:pk>/loeschen/', views.CommentaryDeleteView.as_view(), name='deleteCommentary'),
    path('Zutat/hinzufuegen/', views.CreateGroceryView.as_view(), name='addGrocery'),
    path('Zutat/<int:pk>/bearbeiten/', views.UpdateGroceryView.as_view(), name='updateGrocery'),
    path('Zutat/<int:pk>/loeschen/', views.DeleteGroceryView.as_view(), name='deleteGrocery'),
    path('MeinProfil/', views.MyProfil.as_view(), name='myprofil'),
    path('MeinWochenplan/<int:pk>/', views.Agenda.as_view(), name='agenda'),
    path('Einkaufsliste/<int:pk>/', views.Shopping.as_view(), name='shopping'),
    path('Essensplan/', views.foodplan, name='foodplan'),
    path('Impressum/', views.imprint, name='imprint'),
    path('Essensplan/<int:pk>/loeschen/', views.DeleteFoodplanView.as_view(), name='foodplanDelete'),
]
