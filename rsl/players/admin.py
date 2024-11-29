from django.contrib import admin

from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'number', 'position', 'played', 'goals', 'assists', 'yellow_cards', 'red_cards']