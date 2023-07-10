
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

        def import_games(data):
            # games = Game.objects.all().values()
            # print(data)
            for i,x in data.items():
                # créer le sondage
                new_poll = Poll()
                new_poll.save()
                # récupérer l'id du sondage créé
                new_game = Game(game_title=x['title'], game_date=x['date'], game_time=x['time'], game_place=x['place'], game_coordinates=x['coordinates'], game_poll_id=new_poll.id, game_type=x['type'], game_season=x['season'])
                new_game.save()
            print('Nouveau match créé')

        # Emplacement du fichier 
        # import_type = 'joueurs' # joueurs ou matchs
        title = input('Nom du match : ')
        date = input('Date (format yyyy-mm-dd) : ')
        time = input('Heure (format hh:mm) : ')
        place = input('Lieu : ')
        latitude = input('Latitude du terrain : ')
        longitude = input('Longitude du terrain : ')
        type = input('Compétition (amical, championnat, coupe) : ')
        season = input('Saison : ')
        data = {'title': title, 'date': date, 'time': time, 'place': place, 'coordinates': [latitude, longitude], 'type': type, 'season': season}

        # confirmation de l'import
        print(data)
        confirmation = input('Voici les données à importer. Ok ? (y|n)')

        if confirmation == 'y':
            import_games(data)
        else:
            print('abandon')
