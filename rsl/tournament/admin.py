from django.contrib import admin

from .models import Team, Clasification


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'club_code', 'shield']

@admin.register(Clasification)
class ClasificationAdmin(admin.ModelAdmin):
    list_display = ['team', 'points', 'played', 'wins', 'draws', 'loses', 'goals_scored', 'goals_conceded', 'goals_difference']
