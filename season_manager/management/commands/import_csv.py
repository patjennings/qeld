
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

        def import_players(data):
            # games = Game.objects.all().values()
            # print(data)
            for i,x in data.items():
                # récupérer l'id du sondage créé
                new_player = Player(first_name=x['first_name'], second_name=x['second_name'], status=x['status'])
                new_player.save()
            print('Joueurs importés')

        def import_games(data):
            # games = Game.objects.all().values()
            # print(data)
            for i,x in data.items():
                # créer le sondage
                new_poll = Poll(poll_season=x['season'])
                new_poll.save()
                # récupérer l'id du sondage créé
                new_game = Game(game_title=x['title'], game_date=x['date'], game_time=x['time'], game_place=x['place'], game_poll_id=new_poll.id, game_type=x['type'], game_season=x['season'], game_team_away=x['team_away'], game_team_home=x['team_home'])
                new_game.save()
            print('Matchs importés')

        # Emplacement du fichier 
        path = input('Chemin du fichier : ')
        import_type = input('quelles données ont importées ? (joueurs=j | matchs = m) ')
        data = {}
        with open(path) as f:
            reader = csv.reader(f)
            if import_type == 'j':
                for i,row in enumerate(reader):
                    if i != 0: # skip header
                        data[i] = {'first_name': row[0], 'second_name': row[1], 'status': int(row[2])}
            elif import_type == 'm':
                for i,row in enumerate(reader):
                    if i != 0: # skip header
                        data[i] = {'team_home': row[0], 'team_away': row[1], 'title': row[0]+' — '+row[1], 'date': row[2], 'time': row[3], 'place': row[4], 'type': row[5], 'season': row[6]}

        # confirmation de l'import
        for i in data:
            print(data[i])
        confirmation = input('Voici les données à importer. Ok ? (y|n) ')

        if confirmation == 'y':
            if import_type == 'j':
                import_players(data)
            elif import_type == 'm':
                import_games(data)
        else:
            print('abandon')
