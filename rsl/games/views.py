from django.shortcuts import render
from games.models import Game, Event
from tournament.models import Team

from .forms import AddGameForm, EditGameForm, AddEventForm
from django.shortcuts import redirect, render
from shared.funcs import admin_required


def games(request):
    games = Game.objects.all()
    teams = Team.objects.all()
    return render(request, 'games/games.html', {'games': games, 'teams': teams})


def game_info(request, game_id):
    game = Game.objects.get(id=game_id)
    events = Event.objects.filter(game=game)
    return render(request, 'games/game_info.html', {'game': game, 'events': events})

@admin_required
def add_game(request):
    if request.method == 'POST':
        if (form := AddGameForm(request.POST)).is_valid():
            game = form.save(commit=False)
            game.save()
            return redirect('games:games')
    else:
        form = AddGameForm()
    return render(request, 'games/form.html', {'form': form})

@admin_required
def edit_game(request, game_id):
    game = Game.objects.get(id=game_id)
    if request.method == 'POST':
        if (form := EditGameForm(request.POST, instance=game)).is_valid():
            g = form.save(commit=False)
            g.save()
            return redirect('games:games')
    else:
        form = EditGameForm(instance=game)
    return render(request, 'games/form.html', {'form': form})

@admin_required
def delete_game(request, game_id):
    game = Game.objects.get(id=game_id)
    game.delete()
    return redirect('games:games')

@admin_required   
def add_event(request, game_id):
    game = Game.objects.get(id=game_id)
    if request.method == 'POST':
        if (form := AddEventForm(game, request.POST)).is_valid():
            event = form.save()
            return redirect('games:game-info', game_id)
    else:
            form = AddEventForm(game)
    return render(request, 'games/form.html', {'form': form, 'game': game})

@admin_required
def delete_event(request, game_id, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect('games:game-info', game_id)

def point_game(request, game_id):
    game = Game.objects.get(id=game_id)
    game.point_game()
    return redirect('games:game-info', game_id)
