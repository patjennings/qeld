from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Game,Convocation,Player

# Create your views here.
def games(request):
    games = Game.objects.all().values()

    print(games)

    template = loader.get_template('games.html')
    context = {
        'games': games
    }

    return HttpResponse(template.render(context, request))

def game(request, id):
    game = Game.objects.get(id=id)

    template = loader.get_template('game.html')
    context = {
        'game_title': game.game_title
    }

    return HttpResponse(template.render(context, request))
