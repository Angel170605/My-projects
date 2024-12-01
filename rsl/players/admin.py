from django.contrib import admin

from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'birthdate', 'country', 'number', 'position', 'played', 'goals', 'assists', 'yellow_cards', 'red_cards']