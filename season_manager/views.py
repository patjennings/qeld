from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Game,Poll,Player
# from datetime import datetime, date, time
import datetime
from var_dump import var_dump

__season = '2023-2024'

# Create your views here.
def games(request):
    games = Game.objects.all().values()
    print(__season)

    games_list = []
    present_for_game = {}
    absent_for_game = {}

    current_date = datetime.datetime.now()

    for game in games:
        if game['game_season'] == __season:
            games_list.append(game)

    sorted_games_list = sorted(games_list, key=lambda item:item['game_date'])

    # comparer maintenant avec le match, et retirer ce qui est passé
    for g in sorted_games_list:
        match_date = g['game_date']
        match_time = datetime.time(10, 30)
        match_datetime = datetime.datetime.combine(match_date, match_time)
        if current_date > match_datetime:
            sorted_games_list.remove(g)


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
    display_season = request.GET.get('display_season')

    # check la saison affichée
    current_season = __season
    if display_season != None:
        current_season = display_season

    games_list = []

    for game in games:
        if game['game_season'] == current_season:
            games_list.append(game)

    sorted_games_list = sorted(games_list, key=lambda item:item['game_date'])

    template = loader.get_template('results.html')
    context = {
        'games': sorted_games_list,
    }

    return HttpResponse(template.render(context, request))

def stats(request):
    games = Game.objects.all().values()
    players = Player.objects.all().values()
    polls = Poll.objects.all().values()

    # check la saison affichée
    display_season = request.GET.get('display_season')
    current_season = __season
    if display_season != None:
        current_season = display_season

    strikers = {}
    passers = {}

    games_amical = []
    games_championnat = []
    games_coupe = []

    games_amical_total = 0
    games_championnat_total = 0
    games_coupe_total = 0

    amical_goals_for = 0
    amical_goals_against = 0
    championnat_goals_for = 0
    championnat_goals_against = 0
    coupe_goals_for = 0
    coupe_goals_against = 0
    total_competition_goals_for = 0
    total_all_goals_for = 0
    total_competition_goals_against = 0
    total_all_goals_against = 0
    total_competition_games = 0
    total_all_games = 0
    ratio_all_for = 0
    ratio_competition_for = 0
    ratio_all_against = 0
    ratio_competition_against = 0

    for player in players:
        strikers[player['id']] = {'presence': 0, 'goals': 0}
        passers[player['id']] = {'presence': 0, 'assists': 0}

    for game in games:
        if game['game_season'] == current_season:
            for goals in game['game_goals']:
                strikers[goals]['goals'] += 1
            for assists in game['game_assists']:
                passers[assists]['assists'] += 1
            if game['game_type'] == 'championnat':
                games_championnat.append(game)
            if game['game_type'] == 'coupe':
                games_coupe.append(game)
            if game['game_type'] == 'amical':
                games_amical.append(game)

    for game in games_amical:
        amical_goals_for += game['goals_for']
        amical_goals_against += game['goals_against']
        games_amical_total += 1
    for game in games_championnat:
        championnat_goals_for += game['goals_for']
        championnat_goals_against += game['goals_against']
        games_championnat_total += 1
    for game in games_coupe:
        coupe_goals_for += game['goals_for']
        coupe_goals_against += game['goals_against']
        games_coupe_total += 1

    for poll in polls:
        if poll['poll_season'] == current_season:
            for present in poll['present']:
                strikers[present]['presence'] +=1
                passers[present]['presence'] +=1

    total_competition_goals_for = championnat_goals_for + coupe_goals_for
    total_all_goals_for = amical_goals_for + championnat_goals_for + coupe_goals_for
    total_competition_goals_against = championnat_goals_against + coupe_goals_against
    total_all_goals_against = amical_goals_against + championnat_goals_against + coupe_goals_against
    total_competition_games = games_championnat_total + games_coupe_total
    total_all_games = games_amical_total + games_championnat_total + games_coupe_total
    if total_all_games > 0:
        ratio_all_for = "{:.2f}".format(total_all_goals_for/total_all_games)
        ratio_all_against = "{:.2f}".format(total_all_goals_against/total_all_games)
    if total_competition_games > 0:
        ratio_competition_for = "{:.2f}".format(total_competition_goals_for/total_competition_games)
        ratio_competition_against = "{:.2f}".format(total_competition_goals_against/total_competition_games)

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
        'passers': sorted_passers_dict,
        'games_amical_total': games_amical_total,
        'games_championnat_total': games_championnat_total,
        'games_coupe_total': games_coupe_total,
        'amical_goals_for': amical_goals_for,
        'amical_goals_against': amical_goals_against,
        'championnat_goals_for': championnat_goals_for,
        'championnat_goals_against': championnat_goals_against,
        'coupe_goals_for': coupe_goals_for,
        'coupe_goals_against': coupe_goals_against,
    'total_competition_goals_for': total_competition_goals_for,
    'total_all_goals_for': total_all_goals_for,
    'total_competition_goals_against': total_competition_goals_against,
    'total_all_goals_against': total_all_goals_against,
    'total_competition_games': total_competition_games,
    'total_all_games': total_all_games,
    'ratio_all_for': ratio_all_for,
    'ratio_competition_for': ratio_competition_for,
    'ratio_all_against': ratio_all_against,
    'ratio_competition_against': ratio_competition_against,
    }

    return HttpResponse(template.render(context, request))

def get_player_name(id):
    player = Player.objects.get(id=id)
    player_full_name = player.first_name+' '+player.second_name
    return player_full_name
