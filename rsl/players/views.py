from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from tournament.models import Team
from players.models import Player

from .forms import SignPlayerForm, EditPlayerForm

from .funcs import get_player_age
from shared.funcs import admin_required

def player_list(request):
    players = Player.objects.all()
    return render(request, 'players/player_list.html', {'players': players })


def player_info(request, player_id):
    player = Player.objects.get(id=player_id)
    age = get_player_age(player.birthdate)
    return render(request, 'players/player.html', {'player': player, 'age': age})

@admin_required
def sign_player(request, team_id, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
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
    return render(request, 'players/form.html', {'form': form, 'team': team, 'user': user})

@admin_required
def edit_player(request, player_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    player = Player.objects.get(id=player_id)
    if request.method == 'POST':
        if (form := EditPlayerForm(request.POST, instance=player)).is_valid():
            p = form.save(commit=False)
            p.save()
            return redirect('players:players')
    else:
        form = SignPlayerForm(instance=player)
    return render(request, 'players/form.html', {'form': form})

@admin_required
def delete_player(request, player_id):
    player = Player.objects.get(id=player_id)
    player.delete()
    return redirect('players:player-list')
