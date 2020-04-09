from django.urls import path, include

from . import  views

app_name = 'foodApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.RecipesListView.as_view(), name='recipesList'),
    path('recipes/<int:pk>/', views.RecipesDetailView.as_view(), name='recipesDetail'),
    path('Essenplan/', views.foodplan, name='foodplan'),
] 