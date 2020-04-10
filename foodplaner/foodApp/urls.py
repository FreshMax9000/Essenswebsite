from django.urls import path, include

from . import views

app_name = 'foodApp'
urlpatterns = [
    path('', views.home, name='home'),
    #path('foodplaner/', views.FoodplanerView.as_view(), name='foodplaner'),
    path('Rezepte/', views.RecipesListView.as_view(), name='recipesList'),
    path('Rezepte/<int:pk>/', views.RecipesDetailView.as_view(), name='recipesDetail'),
    path('MeinProfil/', views.myprofil.as_view(), name='myprofil'),
    path('Wochenplan/', views.agenda.as_view(), name='agenda'),
    path('Einkaufsliste/', views.shopping.as_view(), name='shopping'),
] 