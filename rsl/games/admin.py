from django.contrib import admin
from .models import Game, Event

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['local', 'away', 'local_goals', 'away_goals', 'is_league_game']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['game', 'minute', 'player', 'second_player', 'type']
