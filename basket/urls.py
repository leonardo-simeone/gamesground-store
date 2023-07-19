from django.urls import path
from . import views

urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/<game_id>/', views.add_to_basket, name='add_to_basket'),
    path('adjust/<game_id>/', views.adjust_basket, name='adjust_basket'),
    path('remove/<game_id>/', views.remove_from_basket, name='remove_from_basket'),
]
