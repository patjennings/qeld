from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Game,Poll,Player

# Create your views here.
def games(request):
    games = Game.objects.all().values()

    present_for_game = {}
    absent_for_game = {}

    for game in games:
        # print(game['poll_id'])
        poll = Poll.objects.get(id=game['poll_id'])
        present_for_game[game['id']] = len(poll.present)
        absent_for_game[game['id']] = len(poll.absent)

    template = loader.get_template('games.html')
    context = {
        'games': games,
        'present_for_game': present_for_game,
        'absent_for_game': absent_for_game
    }

    return HttpResponse(template.render(context, request))

def game(request, id):
    game = Game.objects.get(id=id)
    players = Player.objects.all().values()
    poll = Poll.objects.get(id=game.poll_id)

    # poll_present = []
    # poll_absent = []
    # poll_audience = []

    poll_present = {}
    poll_absent = {}
    poll_audience = {}

    players_list = {}
    players_poll_done = []

    for p in players:
        if p['status'] is True:
            players_list[p['id']] = p['first_name']+' '+p['second_name']

    for pr in poll.present:
        poll_present[pr] = players.get(id=pr)['first_name']+' '+players.get(id=pr)['second_name']
    for ab in poll.absent:
        poll_absent[ab] = players.get(id=ab)['first_name']+' '+players.get(id=ab)['second_name']
    for au in poll.audience:
        poll_audience[au] = players.get(id=au)['first_name']+' '+players.get(id=au)['second_name']

    for i,p in poll_present.items():
        if i not in players_poll_done:
            players_poll_done.append(i)
    for i,p in poll_absent.items():
        if i not in players_poll_done:
            players_poll_done.append(i)
    for i,p in poll_audience.items():
        if i not in players_poll_done:
            players_poll_done.append(i)

    template = loader.get_template('game.html')
    context = {
        'game': game,
        'players_list': players_list,
        'poll_present': poll_present,
        'poll_absent': poll_absent,
        'poll_audience': poll_audience,
        'players_poll_done': players_poll_done
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

    return HttpResponseRedirect("/game/"+str(game_id))
    # if this is a POST request we need to process the form data


def results(request):
    games = Game.objects.all().values()

    template = loader.get_template('results.html')
    context = {
        'games': games,
    }

    return HttpResponse(template.render(context, request))

def stats(request):
    games = Game.objects.all().values()
    players = Player.objects.all().values()
    polls = Poll.objects.all().values()

    strikers = {}
    passers = {}

    for player in players:
        strikers[player['id']] = {'presence': 0, 'goals': 0}
        passers[player['id']] = {'presence': 0, 'assists': 0}

    for game in games:
        for goals in game['game_goals']:
            strikers[goals]['goals'] += 1
        for assists in game['game_assists']:
            passers[assists]['assists'] += 1

    for poll in polls:
        for present in poll['present']:
            strikers[present]['presence'] +=1
            passers[present]['presence'] +=1
    
    sorted_strikers = sorted(strikers.items(), key=lambda item: item[1]['goals'], reverse=True)
    sorted_strikers_dict = {}
    for key,value in sorted_strikers:
        sorted_strikers_dict[key] = value

    sorted_passers = sorted(passers.items(), key=lambda item: item[1]['assists'], reverse=True)
    sorted_passers_dict = {}
    for key,value in sorted_passers:
        sorted_passers_dict[key] = value


    template = loader.get_template('stats.html')
    context = {
        'players': players,
        'strikers': sorted_strikers_dict,
        'passers': sorted_passers_dict
    }

    return HttpResponse(template.render(context, request))
