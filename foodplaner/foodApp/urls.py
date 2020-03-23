from django.urls import path, include

from . import  views

app_name = 'foodApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/<int:pk>/', views.RecipesView.as_view(), name='recipes'),
] 