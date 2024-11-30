from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.db.models import Q

from players.models import Player
from tournament.models import Match, Team, Event

from .forms import AddTeamForm, EditTeamForm, SignPlayerForm, AddMatchForm, AddEventForm


def main(request):
    return render(request, 'tournament/main.html')


def info(request):
    return render(request, 'tournament/info.html')


def teams(request):
    teams = Team.objects.all()
    return render(request, 'tournament/teams.html', {'teams': teams})


def team_info(request, team_id):
    team = Team.objects.get(id=team_id)
    users = User.objects.all()
    players = Player.objects.filter(team=team)
    matches = Match.objects.filter(Q(local=team) | Q(away=team))
    return render(
        request, 'tournament/team.html', {'team': team, 'users': users, 'players': players, 'matches': matches}
    )

def matches(request):
    matches = Match.objects.all()
    teams = Team.objects.all()
    return render(request, 'tournament/matches.html', {'matches': matches, 'teams': teams})

def match_info(request, match_id):
    match = Match.objects.get(id=match_id)
    events = Event.objects.filter(game=match)
    return render(request, 'tournament/match_info.html', {'match': match, 'events': events})

def add_team(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    if request.method == 'GET':
        form = AddTeamForm()
    else:
        if (form := AddTeamForm(request.POST, request.FILES)).is_valid():
            form.save()
            return redirect('tournament:teams')
    return render(request, 'tournament/form.html', {'form': form})


def edit_team(request, team_id):
    team = Team.objects.get(id=team_id)
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    if request.method == 'GET':
        form = EditTeamForm(instance=team)
    else:
        if (form := EditTeamForm(request.POST, request.FILES, instance=team)).is_valid():
            team = form.save()
            return redirect('tournament:teams')
    return render(request, 'tournament/form.html', {'team': team, 'form': form})


def delete_team(request, team_id):
    team = Team.objects.get(id=team_id)
    team.delete()
    return redirect('tournament:teams')


def sign_player(request, team_id, user_id):
    team = Team.objects.get(id=team_id)
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        if (form := SignPlayerForm(request.POST)).is_valid():
            player = form.save(commit=False)
            player.user = user
            player.team = team
            player.save()
            return redirect('tournament:team-info', team_id)
    else:
        form = SignPlayerForm()
    return render(request, 'tournament/form.html', {'form': form, 'team': team, 'user': user})

def add_match(request):
    if request.method == 'POST':
        if (form := AddMatchForm(request.POST)).is_valid():
            game = form.save(commit=False)
            game.save()
            return redirect('tournament:matches')
    else:
        form = AddMatchForm()
    return render(request, 'tournament/form.html', {'form': form})
    
    
def add_event(request, match_id):
    game = Match.objects.get(id=match_id)
    if request.method == 'POST':
        if (form := AddEventForm(request.POST)).is_valid():
            event = form.save(commit=False)
            event.game = game
            event.save()
            return redirect('tournament:match-info', match_id)
    else:
            form = AddEventForm()
    return render(request, 'tournament/form.html', {'form': form, 'game': game})

