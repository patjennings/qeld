from django.urls import path
from . import views

urlpatterns = [
    path('matchs/', views.matchs, name='matchs'),
]
