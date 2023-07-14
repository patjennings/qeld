from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.games, name='games'),
    path('results/', views.results, name='results'),
    path('stats/', views.stats, name='stats'),
    path('game/<int:id>', views.game, name='game'),
    path('game/<int:id>/update_game_stats/', views.update_game_stats, name='update_game_stats'),
    path('poll_answer/<int:id>', views.poll_answer, name='poll_answer')
    # path('games/game/<int:id>/delete', views.game_delete, name='game_delete'),
]
