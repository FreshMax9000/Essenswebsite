from django.urls import path, include

from . import  views

app_name = 'foodApp'
urlpatterns = [
    path('', views.home, name='home'),
    #path('foodplaner/', views.FoodplanerView.as_view(), name='foodplaner'),
    path('recipes/', views.RecipesListView.as_view(), name='recipesList'),
    path('recipes/<int:pk>/', views.RecipesDetailView.as_view(), name='recipesDetail'),
] 