from django.urls import path
from . import views

urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/<game_id>', views.add_to_basket, name='add_to_basket'),
]
