from django.urls import path

from . import views

app_name = 'foodApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('design2', views.home_design2, name='home_design2'),
    path('Suche', views.RecipesListView.as_view(), name='recipesList'),
    path('Verifizieren', views.ReviewRecipesListView.as_view(), name='reviewRecipesList'),
    path('Rezepte/<int:pk>/', views.RecipesDetailView.as_view(), name='recipesDetail'),
    path('Rezepte/<int:pk>/loeschen/', views.DeleteRecipeView.as_view(), name='recipesDelete'),
    path('Rezepte/<int:pk>/bearbeiten/', views.UpdateRecipeView.as_view(), name='recipesUpdate'),
    path('Rezepte/hinzufuegen/', views.CreateRecipeView.as_view(), name='addRecipe'),
    path('Zutat/hinzufuegen/', views.CreateGroceryView.as_view(), name='addGrocery'),
    path('Zutat/<int:pk>/bearbeiten/', views.UpdateGroceryView.as_view(), name='updateGrocery'),
    path('Zutat/<int:pk>/loeschen/', views.DeleteGroceryView.as_view(), name='deleteGrocery'),
    path('MeinProfil/', views.MyProfil.as_view(), name='myprofil'),
    path('MeinWochenplan/<int:pk>/', views.Agenda.as_view(), name='agenda'),
    path('Einkaufsliste/<int:pk>/', views.Shopping.as_view(), name='shopping'),
    path('Essensplan/', views.foodplan, name='foodplan'),
    path('Essensplan/<int:pk>/loeschen/', views.DeleteFoodplanView.as_view(), name='foodplanDelete'),
]
