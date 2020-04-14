from django.urls import path, include

from . import views

app_name = 'foodApp'
urlpatterns = [
    path('', views.home, name='home'),
    # path('foodplaner/', views.FoodplanerView.as_view(), name='foodplaner'),
    path('Rezepte/', views.RecipesListView.as_view(), name='recipesList'),
    path('Rezepte/<int:pk>/', views.RecipesDetailView.as_view(), name='recipesDetail'),
    path('Rezepte/<int:pk>/loeschen/', views.DeleteRecipeView.as_view(), name='recipesDelete'),
    path('Rezepte/<int:pk>/bearbeiten/', views.UpdateRecipeView.as_view(), name='recipesUpdate'),
    path('Rezepte/hinzufuegen/', views.CreateRecipeView.as_view(), name='addRecipe'),
    path('MeinProfil/', views.MyProfil, name='myProfil'),
    path('Wochenplan/', views.Wochenplan, name='Wochenplan'),
    path('Zutat_hinzufuegen/', views.CreateGroceryView.as_view(), name='addGrocery'),
]
