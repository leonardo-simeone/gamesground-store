from django.urls import path
from . import views

urlpatterns = [
    path('', views.games, name='games'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('like_game/<int:game_id>/', views.like_game, name='like_game'),
    path('add/', views.add_game, name='add_game'),
    path('edit/<int:game_id>/', views.edit_game, name='edit_game'),
    path('delete/<int:game_id>/', views.delete_game, name='delete_game'),
]
