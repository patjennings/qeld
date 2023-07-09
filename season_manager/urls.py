from django.urls import path
from . import views

urlpatterns = [
    path('games/', views.games, name='games'),
    path('games/game/<int:id>', views.game, name='game'),
    # path('games/game/<int:id>/delete', views.game_delete, name='game_delete'),
]
