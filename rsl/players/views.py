from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from tournament.models import Team
from players.models import Player

from .forms import SignPlayerForm, EditPlayerForm

from shared.funcs import admin_required, get_player_age

def player_info(request, player_id):
    player = Player.objects.get(id=player_id)
    if player.birthdate:
        age = get_player_age(player.birthdate)
    else:
        age = ''
    return render(request, 'players/player.html', {'player': player, 'age': age})

@admin_required
def sign_player(request, team_id, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    team = Team.objects.get(id=team_id)
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        if (form := SignPlayerForm(request.POST, request.FILES)).is_valid():
            player = form.save(commit=False)
            player.user = user
            player.team = team
            player.save()
            return redirect('tournament:team-info', team_id)
    else:
        form = SignPlayerForm()
    return render(request, 'players/form.html', {'form': form, 'team': team, 'user': user})

@admin_required
def edit_player(request, player_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    player = Player.objects.get(id=player_id)
    if request.method == 'POST':
        if (form := EditPlayerForm(request.POST, request.FILES, instance=player)).is_valid():
            p = form.save(commit=False)
            p.save()
            return redirect('players:player-info', player_id)
    else:
        form = SignPlayerForm(instance=player)
    return render(request, 'players/form.html', {'form': form})

@admin_required
def delete_player(request, player_id):
    player = Player.objects.get(id=player_id)
    team_id = player.team.id
    player.delete()
    return redirect('tournament:team-info', team_id)
