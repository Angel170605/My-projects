from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from tournament.models import Team

from .forms import SignPlayerForm

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
