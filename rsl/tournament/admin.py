from django.contrib import admin

from .models import Match, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'club_code', 'shield']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['local', 'away', 'local_goals', 'away_goals']
