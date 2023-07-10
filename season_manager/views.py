from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Game,Poll,Player
from datetime import datetime
from var_dump import var_dump

__season = '2023-2024'

# Create your views here.
def games(request):
    games = Game.objects.all().values()
    print(__season)

    games_list = []
    present_for_game = {}
    absent_for_game = {}

    current_date = datetime.now()


    for game in games:
        # print(game['game_season'], __season)
        if game['game_season'] == __season:
            games_list.append(game)

    # print(games_list)
    print(games_list)
    # for i,d in games_list.items():
        # print(d['game_date'])

    sorted_games_list = sorted(games_list, key=lambda item:item['game_date'])


    for g in sorted_games_list:
        print(current_date, datetime.date(g['game_date']))
        # if g['game_date'] < datetime.date.now():
            # sorted_games_list.remove(g)
    # sorted_game_list_dict = {}
    # for key,value in sorted_game_list:
        # sorted_game_list_dict[key] = value

    # sorted_strikers = sorted(strikers.items(), key=lambda item: item[1]['goals'], reverse=True)
    # sorted_strikers_dict = {}
    # for key,value in sorted_strikers:
        # sorted_strikers_dict[key] = value

    for game in games:
        poll = Poll.objects.get(id=game['game_poll_id'])
        present_for_game[game['id']] = len(poll.present)
        absent_for_game[game['id']] = len(poll.absent)

    template = loader.get_template('games.html')
    context = {
        'games': sorted_games_list,
        'present_for_game': present_for_game,
        'absent_for_game': absent_for_game
    }

    return HttpResponse(template.render(context, request))

def game(request, id):
    game = Game.objects.get(id=id)
    players = Player.objects.all().values()
    poll = Poll.objects.get(id=game.game_poll_id)

    poll_present = {}
    poll_absent = {}
    poll_audience = {}

    players_list = {}
    players_poll_done = []

    for p in players:
        if p['status'] is True:
            players_list[p['id']] = get_player_name(p['id'])

    for pr in poll.present:
        poll_present[pr] = get_player_name(pr)
    for ab in poll.absent:
        poll_absent[ab] = get_player_name(ab)
    for au in poll.audience:
        poll_audience[au] = get_player_name(au)

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

def update_game_stats(request, id):
    game_id = request.GET.get('game')
    player_id = request.GET.get('player')
    field = request.GET.get('field')
    method = request.GET.get('method')

    player_name = get_player_name(int(player_id))
    game = Game.objects.get(id=game_id)

    def add_stat(s, p):
        game_stat = getattr(game, s)
        game_stat.append(p)
        game.save()
    def remove_stat(s, p):
        game_stat = getattr(game, s)
        # i=len(game_stat)
        # while i > 0:
            # if i is p:
                # del game_stat[i]
                # print(game_stat[i])
                # game.save()
                # break
            # i-=1

        for i in game_stat:
            # print(i)
            if i is p:
                game_stat.remove(p)
                game.save()
                break
                # print('remove')
            # else:
                # print('nope')

    if method == 'add':
        add_stat(field, int(player_id))
    elif method == 'remove':
        remove_stat(field, int(player_id))

    return HttpResponseRedirect("/game/"+str(game_id))

def poll_answer(request, id):
    game_id = request.GET.get('game')
    player_id = request.GET.get('player')
    game_poll_id = request.GET.get('poll')
    answer_status = request.GET.get('status')

    game = Game.objects.get(id=game_id)
    player = Player.objects.get(id=player_id)
    poll = Poll.objects.get(id=game_poll_id)

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

    print(strikers) 

    template = loader.get_template('stats.html')
    context = {
        'players': players,
        'strikers': sorted_strikers_dict,
        'passers': sorted_passers_dict
    }

    return HttpResponse(template.render(context, request))

def get_player_name(id):
    player = Player.objects.get(id=id)
    player_full_name = player.first_name+' '+player.second_name
    return player_full_name
