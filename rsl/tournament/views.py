from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from players.models import Player
from tournament.models import Team

from .forms import AddTeamForm, EditTeamForm, SignPlayerForm


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
    return render(
        request, 'tournament/team.html', {'team': team, 'users': users, 'players': players}
    )


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


def edit_team(request, name: str):
    team = Team.objects.get(name=name)
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    if request.method == 'GET':
        form = EditTeamForm(instance=team)
    else:
        if (form := EditTeamForm(request.POST, request.FILES, instance=team)).is_valid():
            team = form.save()
            return redirect('tournament:teams')
    return render(request, 'tournament/form.html', {'team': team, 'form': form})


def delete_team(request, name: str):
    team = Team.objects.get(name=name)
    team.delete()
    return redirect('tournament:teams')


def sign_player(request, team_id, user_id):
    team = Team.objects.get(id=team_id)
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = SignPlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = user
            player.team = team
            player.save()
            return redirect('tournament:team-info', team_id)
    else:
        form = SignPlayerForm()
    return render(request, 'tournament/form.html', {'form': form, 'team': team, 'user': user})
