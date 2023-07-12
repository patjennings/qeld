from django.db import models
from datetime import date

# Create your models here.
class Poll(models.Model):
    present = models.CharField(max_length=255, default='[]')
    absent = models.CharField(max_length=255, default='[]')
    audience = models.CharField(max_length=255, default='[]')
    poll_season = models.CharField(max_length=255,default='')

class Game(models.Model):
    game_title = models.CharField(max_length=255)
    game_team_home = models.CharField(max_length=255, default='')
    game_team_away = models.CharField(max_length=255, default='')
    game_date = models.DateField(default=date.today)
    game_time = models.CharField(max_length=255, default='10:00')
    game_score = models.CharField(max_length=255, default='0-0')
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    game_goals = models.CharField(max_length=255, default='[]')
    game_assists = models.CharField(max_length=255, default='[]')
    game_redcards = models.CharField(max_length=255, default='[]')
    game_yellowcards = models.CharField(max_length=255, default='[]')
    game_status = models.CharField(max_length=255, default='planned')
    game_type = models.CharField(max_length=255)
    game_place = models.CharField(max_length=255,default='None')
    game_coordinates = models.CharField(max_length=255, default='[]')
    game_poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    game_season = models.CharField(max_length=255,default='')

class Player(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    status = models.BooleanField()


