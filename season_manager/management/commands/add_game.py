
# run script within django
# python manage.py shell < scripts/add_images.py
import csv
import sys
from os import listdir, remove
from os.path import isfile, join, getctime, getmtime, splitext
import shutil
from django.db import models
from django.core.management.base import BaseCommand, CommandError
# from .models import Game
from season_manager.models import Game,Poll,Player
# from .models import Player
# from .models import Poll
from datetime import datetime
import subprocess

class Command(BaseCommand):
    help = 'import a csv with games or players into Qeld'

    def handle(self, *args, **options):

        def add_game(data):
            # games = Game.objects.all().values()
            # créer le sondage
            new_poll = Poll(poll_season=data['season'])
            new_poll.save()
            # récupérer l'id du sondage créé
            new_game = Game(game_title=data['title'], game_date=data['date'], game_time=data['time'], game_place=data['place'], game_poll_id=new_poll.id, game_type=data['type'], game_season=data['season'], game_team_home=data['team_home'], game_team_away=data['team_away'])
            new_game.save()
            print('Nouveau match créé')

        # Emplacement du fichier 
        # import_type = 'joueurs' # joueurs ou matchs
        team_home = input('Équipe qui reçoit : ')
        team_away = input('Équipe qui se déplace : ')
        date = input('Date (format yyyy-mm-dd) : ')
        time = input('Heure (format hh:mm:ss) : ')
        place = input('Lieu (slug): ')
        type = input('Compétition (amical, championnat, coupe) : ')
        season = input('Saison : ')
        title = team_home+' — '+team_away
        data = {'title': title, 'date': date, 'time': time, 'place': place, 'type': type, 'season': season, 'team_home': team_home, 'team_away': team_away}

        # confirmation de l'import
        print(data)
        confirmation = input('Voici les données à importer. Ok ? (y|n)')

        if confirmation == 'y':
            add_game(data)
        else:
            print('abandon')
