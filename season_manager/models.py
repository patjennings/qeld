from django.db import models
from datetime import date

# Create your models here.
class Poll(models.Model):
    present = models.CharField(max_length=255, default='[]')
    absent = models.CharField(max_length=255, default='[]')
    audience = models.CharField(max_length=255, default='[]')
    poll_season = models.CharField(max_length=255,default='')

class Player(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    status = models.BooleanField()
    def full_name(self):
        full_name = self.first_name+' '+self.second_name
        return full_name

class Ground(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    long = models.FloatField()
    city = models.CharField(max_length=255)

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
    game_poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    game_season = models.CharField(max_length=255,default='')
    game_ground = models.ForeignKey(Ground, on_delete=models.CASCADE, null=True)

    def ground_name(self):
        ground = Ground.objects.get(id=self.game_ground.id)
        ground_name = ground.name
        return ground_name


