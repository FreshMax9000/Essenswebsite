from django.urls import path, include

from . import views

app_name = 'foodApp'
urlpatterns = [
    path('', views.home, name='home'),
    #path('foodplaner/', views.FoodplanerView.as_view(), name='foodplaner'),
    path('Rezepte/', views.RecipesListView.as_view(), name='recipesList'),
    path('Rezepte/<int:pk>/', views.RecipesDetailView.as_view(), name='recipesDetail'),
    path('MeinProfil/', views.MyProfil.as_view(), name='myprofil'),
    path('Wochenplan/<int:pk>/', views.Agenda.as_view(), name='agenda'),
    path('Einkaufsliste/', views.Shopping.as_view(), name='shopping'),
] 