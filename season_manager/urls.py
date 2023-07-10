from django.urls import path
from . import views

urlpatterns = [
    path('games/', views.games, name='games'),
    path('results/', views.results, name='results'),
    path('stats/', views.stats, name='stats'),
    path('game/<int:id>', views.game, name='game'),
    path('poll_answer/<int:id>', views.poll_answer, name='poll_answer')
    # path('games/game/<int:id>/delete', views.game_delete, name='game_delete'),
]
