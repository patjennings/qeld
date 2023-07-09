from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Game,Poll,Player

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
    players = Player.objects.all().values()
    poll = Poll.objects.get(id=game.poll_id)

    poll_present = []
    poll_absent = []
    poll_audience = []

    for pr in poll.present:
        poll_present.append(players.get(id=pr)['first_name']+' '+players.get(id=pr)['second_name'])
    for ab in poll.absent:
        poll_absent.append(players.get(id=ab)['first_name']+' '+players.get(id=ab)['second_name'])
    for au in poll.audience:
        poll_audience.append(players.get(id=au)['first_name']+' '+players.get(id=au)['second_name'])

    template = loader.get_template('game.html')
    context = {
        'game': game,
        'players': players,
        'poll_present': poll_present,
        'poll_absent': poll_absent,
        'poll_audience': poll_audience
    }

    return HttpResponse(template.render(context, request))

def poll_answer(request, id):
    game_id = request.GET.get('game')
    player_id = request.GET.get('player')
    poll_id = request.GET.get('poll')
    answer_status = request.GET.get('status')

    game = Game.objects.get(id=game_id)
    player = Player.objects.get(id=player_id)
    poll = Poll.objects.get(id=poll_id)

    poll_present = poll.present
    poll_absent = poll.absent
    poll_audience = poll.audience


    def remove_from_list(id, record, li):
        if int(id) in li:
            li.remove(int(id))
            record = li
            poll.save()

    def add_to_list(id, record, li):
        if int(id) not in li:
            li.append(int(id))
            record = li
            poll.save()

    if answer_status == 'present':
        remove_from_list(player_id, poll.absent, poll_absent)
        remove_from_list(player_id, poll.audience, poll_audience)
        add_to_list(player_id, poll.present, poll_present)
    elif answer_status == 'absent':
        remove_from_list(player_id, poll.present, poll_present)
        remove_from_list(player_id, poll.audience, poll_audience)
        add_to_list(player_id, poll.absent, poll_absent)
    elif answer_status == 'audience':
        remove_from_list(player_id, poll.absent, poll_absent)
        remove_from_list(player_id, poll.present, poll_present)
        add_to_list(player_id, poll.audience, poll_audience)
    else:
        print('erreur')

    return HttpResponseRedirect("/games/game/"+str(game_id))
    # if this is a POST request we need to process the form data

