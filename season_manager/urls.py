from django.urls import path
from . import views

urlpatterns = [
    path('games/', views.games, name='games'),
    path('games/game/<int:id>', views.game, name='game'),
    path('poll_answer/<int:id>', views.poll_answer, name='poll_answer')
    # path('games/game/<int:id>/delete', views.game_delete, name='game_delete'),
]
