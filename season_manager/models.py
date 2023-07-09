from django.db import models
from datetime import date

# Create your models here.
class Convocation(models.Model):
    present = models.JSONField()
    absent = models.JSONField()
    audience = models.JSONField()

class Game(models.Model):
    game_title = models.CharField(max_length=255)
    game_date = models.DateField(default=date.today)
    game_time = models.CharField(max_length=255, default='10:00')
    game_score = models.CharField(max_length=255)
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()
    game_status = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    game_place = models.CharField(max_length=255,default='None')
    game_place_link = models.TextField(default='None')
    convocation = models.ForeignKey(Convocation, on_delete=models.CASCADE)

class Player(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    status = models.BooleanField()


