from django.db import models
from datetime import date

# Create your models here.
class Poll(models.Model):
    present = models.JSONField(default=[])
    absent = models.JSONField(default=[])
    audience = models.JSONField(default=[])
    poll_season = models.CharField(max_length=255,default='')

class Game(models.Model):
    game_title = models.CharField(max_length=255)
    game_date = models.DateField(default=date.today)
    game_time = models.CharField(max_length=255, default='10:00')
    game_score = models.CharField(max_length=255, default='0-0')
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    game_goals = models.JSONField(default=[])
    game_assists = models.JSONField(default=[])
    game_redcards = models.JSONField(default=[])
    game_yellowcards = models.JSONField(default=[])
    game_status = models.CharField(max_length=255, default='planned')
    game_type = models.CharField(max_length=255)
    game_place = models.CharField(max_length=255,default='None')
    game_coordinates = models.JSONField(default=[])
    game_poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    game_season = models.CharField(max_length=255,default='')

class Player(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    status = models.BooleanField()


