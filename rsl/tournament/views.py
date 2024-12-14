from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.db.models import Q

from players.models import Player
from tournament.models import Team
from games.models import Game

from .forms import AddTeamForm, EditTeamForm, SignPlayerForm
from shared.funcs import admin_required


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
    games = Game.objects.filter(Q(local=team) | Q(away=team))
    return render(
        request, 'tournament/team.html', {'team': team, 'users': users, 'players': players, 'games': games}
    )

@admin_required
def add_team(request):
    if request.method == 'GET':
        form = AddTeamForm()
    else:
        if (form := AddTeamForm(request.POST, request.FILES)).is_valid():
            form.save()
            return redirect('tournament:teams')
    return render(request, 'tournament/form.html', {'form': form})

@admin_required
def edit_team(request, team_id):
    team = Team.objects.get(id=team_id)
    if request.method == 'GET':
        form = EditTeamForm(instance=team)
    else:
        if (form := EditTeamForm(request.POST, request.FILES, instance=team)).is_valid():
            team = form.save()
            return redirect('tournament:teams')
    return render(request, 'tournament/form.html', {'team': team, 'form': form})

@admin_required
def delete_team(request, team_id):
    team = Team.objects.get(id=team_id)
    team.delete()
    return redirect('tournament:teams')