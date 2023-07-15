from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Game,Poll,Player
# from datetime import datetime, date, time
import datetime
from var_dump import var_dump
from ast import literal_eval

__season = '2023-2024'

# Create your views here.
def home(request):
    if check_user(request):
        is_admin = True
    else:
        is_admin = False
    template = loader.get_template('home.html')
    context = {
        'title': 'This is les Piliers',
        'is_admin': is_admin
    }

    return HttpResponse(template.render(context, request))


def games(request):
    if check_user(request):
        is_admin = True
    else:
        is_admin = False

    print(is_admin)
    games = Game.objects.all().values()
    print(__season)

    games_list = []
    present_for_game = {}
    absent_for_game = {}


    for game in games:
        if game['game_season'] == __season:
            games_list.append(game)

    sorted_games_list = sorted(games_list, key=lambda item:item['game_date'])

    # comparer maintenant avec le match, et retirer ce qui est passé
    for g in sorted_games_list:
        if is_game_past(g['game_date']):
            sorted_games_list.remove(g)

    for game in games:
        poll = Poll.objects.get(id=game['game_poll_id'])
        present_for_game[game['id']] = len(get_list_from_str(poll.present))
        absent_for_game[game['id']] = len(get_list_from_str(poll.absent))

    template = loader.get_template('games.html')
    context = {
        'games': sorted_games_list,
        'present_for_game': present_for_game,
        'absent_for_game': absent_for_game,
        'is_admin': is_admin
    }

    return HttpResponse(template.render(context, request))

def game(request, id):
    game = Game.objects.get(id=id)
    players = Player.objects.all().order_by('second_name').values()
    poll = Poll.objects.get(id=game.game_poll_id)

    if check_user(request):
        is_admin = True
    else:
        is_admin = False
    # on commence par transformer les strings de la base en vraies listes
    poll_present_list = get_list_from_str(poll.present)
    poll_absent_list = get_list_from_str(poll.absent)
    poll_audience_list = get_list_from_str(poll.audience)

    # on récupère la longueur de chaque liste, pour le compteur dans le template
    present_for_game = len(poll_present_list)
    absent_for_game = len(poll_absent_list)
    staff_for_game = len(poll_audience_list)

    game_status = game.game_status # planned, delayed ou played : planned, delayed, on affiche. Played, on affiche le score

    if is_game_past(game.game_date):
        game_status = 'played'

    poll_present = {}
    poll_absent = {}
    poll_audience = {}

    players_list = {} # la liste des joueurs actifs, pour le sondage
    players_list_full = {} # la liste complète des joueurs, hors actif/non actif, pour garder la trace des buteurs, cartons, etc.
    players_poll_done = []

    for p in players:
        if p['status'] is True:
            players_list[p['id']] = get_player_name(p['id'])
            
    for p in players:
        players_list_full[p['id']] = get_player_name(p['id'])

    for pr in poll_present_list:
        poll_present[pr] = get_player_name(pr)
    for ab in poll_absent_list:
        poll_absent[ab] = get_player_name(ab)
    for au in poll_audience_list:
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


    print(players_list)

    template = loader.get_template('game.html')

    context = {
        'game': game,
        'game_goals': get_list_from_str(game.game_goals),
        'game_assists': get_list_from_str(game.game_assists),
        'game_yellowcards': get_list_from_str(game.game_yellowcards),
        'game_redcards': get_list_from_str(game.game_redcards),
        'players_list': players_list,
        'players_list_full': players_list_full,
        'poll_present': poll_present,
        'poll_absent': poll_absent,
        'poll_audience': poll_audience,
        'present_for_game': present_for_game,
        'absent_for_game': absent_for_game,
        'staff_for_game': staff_for_game,
        'players_poll_done': players_poll_done,
        'status': game_status,
        'is_admin': is_admin
    }

    return HttpResponse(template.render(context, request))

def update_game_stats(request, id):
    game_id = request.GET.get('game')
    player_id = request.GET.get('player')
    field = request.GET.get('field')
    method = request.GET.get('method')

    player_name = get_player_name(int(player_id))
    game = Game.objects.get(id=game_id)

    def add_stat(l, p):
        l.append(p)
        return l

    def remove_stat(l, p):
        for i in l:
            if i is p:
                l.remove(p)
                return l
                break # on break dès qu'on trouve, car on ne 

    if method == 'add':
        game_stat = getattr(game, field) # getattr permet de pointer un champ dans la table, passé par une variable, et de récupérer la donnée
        game_stat_list = get_list_from_str(game_stat)
        game_stat_update = add_stat(game_stat_list, int(player_id))
        game_stat = setattr(game, field, game_stat_update)# setattr permet de pointer un champ dans la table, passé par une variable, et de remplacer la donnée
        game.save()
    elif method == 'remove':
        game_stat = getattr(game, field)
        game_stat_list = get_list_from_str(game_stat)
        game_stat_update = remove_stat(game_stat_list, int(player_id))
        game_stat = setattr(game, field, game_stat_update)
        game.save()

    return HttpResponseRedirect("/game/"+str(game_id))

def poll_answer(request, id):
    game_id = request.GET.get('game')
    player_id = request.GET.get('player')
    game_poll_id = request.GET.get('poll')
    answer_status = request.GET.get('status')

    game = Game.objects.get(id=game_id)
    player = Player.objects.get(id=player_id)
    poll = Poll.objects.get(id=game_poll_id)

    poll_present = get_list_from_str(poll.present)
    poll_absent = get_list_from_str(poll.absent)
    poll_audience = get_list_from_str(poll.audience)

    def remove_from_list(id, li):
        if int(id) in li:
            li.remove(int(id))
            return li
        else:
            return li

    def add_to_list(id, li):
        if int(id) not in li:
            li.append(int(id))
            return li
        else:
            return li

    if answer_status == 'present':
        poll.present = str(add_to_list(player_id, poll_present))
        poll.absent = str(remove_from_list(player_id, poll_absent))
        poll.audience = str(remove_from_list(player_id, poll_audience))
        poll.save()
    elif answer_status == 'absent':
        poll.absent = str(add_to_list(player_id, poll_absent))
        poll.present = str(remove_from_list(player_id, poll_present))
        poll.audience = str(remove_from_list(player_id, poll_audience))
        poll.save()
    elif answer_status == 'audience':
        poll.audience = str(add_to_list(player_id, poll_audience))
        poll.present = str(remove_from_list(player_id, poll_present))
        poll.absent = str(remove_from_list(player_id, poll_absent))
        poll.save()
    else:
        print('erreur')

    return HttpResponseRedirect("/game/"+str(game_id))


def results(request):
    if check_user(request):
        is_admin = True
    else:
        is_admin = False

    games = Game.objects.all().values()
    display_season = request.GET.get('display_season')

    seasons_list = get_seasons_from_games(games)

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
        'is_admin': is_admin,
        'seasons_list' : seasons_list,
        'current_season': __season
    }

    return HttpResponse(template.render(context, request))

def stats(request):

    if check_user(request):
        is_admin = True
    else:
        is_admin = False

    games = Game.objects.all().values()
    players = Player.objects.all().values()
    polls = Poll.objects.all().values()

    seasons_list = get_seasons_from_games(games)

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

    stats = {}
    stats['games_amical_total'] = 0
    stats['games_championnat_total'] = 0
    stats['games_coupe_total'] = 0
    stats['amical_goals_for'] = 0
    stats['amical_goals_against'] = 0
    stats['championnat_goals_for'] = 0
    stats['championnat_goals_against'] = 0
    stats['coupe_goals_for'] = 0
    stats['coupe_goals_against'] = 0
    stats['total_competition_goals_for'] = 0
    stats['total_all_goals_for'] = 0
    stats['total_competition_goals_against'] = 0
    stats['total_all_goals_against'] = 0
    stats['total_competition_games'] = 0
    stats['total_all_games'] = 0
    stats['ratio_all_for'] = 0
    stats['ratio_competition_for'] = 0
    stats['ratio_all_against'] = 0
    stats['ratio_competition_against'] = 0

    print(stats)

    for player in players:
        strikers[player['id']] = {'presence': 0, 'goals': 0}
        passers[player['id']] = {'presence': 0, 'assists': 0}

    for game in games:
        if game['game_season'] == current_season:
            for goals in get_list_from_str(game['game_goals']):
                strikers[goals]['goals'] += 1
            for assists in get_list_from_str(game['game_assists']):
                passers[assists]['assists'] += 1
            if game['game_type'] == 'championnat':
                games_championnat.append(game)
            if game['game_type'] == 'coupe':
                games_coupe.append(game)
            if game['game_type'] == 'amical':
                games_amical.append(game)

    for game in games_amical:
        stats['amical_goals_for'] += game['goals_for']
        stats['amical_goals_against'] += game['goals_against']
        stats['games_amical_total'] += 1
    for game in games_championnat:
        stats['championnat_goals_for'] += game['goals_for']
        stats['championnat_goals_against'] += game['goals_against']
        stats['games_championnat_total'] += 1
    for game in games_coupe:
        stats['coupe_goals_for'] += game['goals_for']
        stats['coupe_goals_against'] += game['goals_against']
        stats['games_coupe_total'] += 1

    for poll in polls:
        if poll['poll_season'] == current_season:
            for present in get_list_from_str(poll['present']):
                strikers[present]['presence'] +=1
                passers[present]['presence'] +=1

    stats['total_competition_goals_for'] = stats['championnat_goals_for'] + stats['coupe_goals_for']
    stats['total_all_goals_for'] = stats['amical_goals_for'] + stats['championnat_goals_for'] + stats['coupe_goals_for']
    stats['total_competition_goals_against'] = stats['championnat_goals_against'] + stats['coupe_goals_against']
    stats['total_all_goals_against'] = stats['amical_goals_against'] + stats['championnat_goals_against'] + stats['coupe_goals_against']
    stats['total_competition_games'] = stats['games_championnat_total'] + stats['games_coupe_total']
    stats['total_all_games'] = stats['games_amical_total'] + stats['games_championnat_total'] + stats['games_coupe_total']
    if stats['total_all_games'] > 0:
        stats['ratio_all_for'] = "{:.2f}".format(stats['total_all_goals_for']/stats['total_all_games'])
        stats['ratio_all_against'] = "{:.2f}".format(stats['total_all_goals_against']/stats['total_all_games'])
    if stats['total_competition_games'] > 0:
        stats['ratio_competition_for'] = "{:.2f}".format(stats['total_competition_goals_for']/stats['total_competition_games'])
        stats['ratio_competition_against'] = "{:.2f}".format(stats['total_competition_goals_against']/stats['total_competition_games'])

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
        'stats': stats,
        'is_admin': is_admin,
        'seasons_list' : seasons_list,
        'current_season': __season
    }

    return HttpResponse(template.render(context, request))

# fonctions utilitaires
def get_player_name(id):
    player = Player.objects.get(id=id)
    player_full_name = player.first_name+' '+player.second_name
    return player_full_name

def get_list_from_str(src_str):
    src_list = src_str
    # src_list = '['+src_str+']'
    out_list = literal_eval(src_list)
    return out_list

def is_game_past(game_date):
    current_date = datetime.datetime.now()
    match_date = game_date
    match_time = datetime.time(10, 30)
    match_datetime = datetime.datetime.combine(match_date, match_time)
    if current_date > match_datetime:
        return True
    else:
        return False

def check_user(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

def get_seasons_from_games(games):
    seasons_list = []
    for game in games:
        # print(game['game_season'])
        if game['game_season'] not in seasons_list:
            seasons_list.append(game['game_season'])

    # sorted_seasons_list = sorted(seasons_list.items(), reverse=True)
    seasons_list.sort(reverse=True)
    return seasons_list
