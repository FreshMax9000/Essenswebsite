from django.urls import path, include

from . import views

app_name = 'foodApp'
urlpatterns = [
    path('', views.home, name='home'),
    #path('foodplaner/', views.FoodplanerView.as_view(), name='foodplaner'),
    path('Rezepte/', views.RecipesListView.as_view(), name='recipesList'),
    path('Rezepte/<int:pk>/', views.RecipesDetailView.as_view(), name='recipesDetail'),
    path('MeinProfil/', views.MyProfil, name='myProfil'),
    path('Wochenplan/', views.Wochenplan, name='Wochenplan'),
] 