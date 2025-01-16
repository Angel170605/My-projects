from django import forms
from django.db.models import Q

from .models import Game, Event
from players.models import Player

class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('local', 'away', 'local_goals', 'away_goals', 'date', 'time')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class EditGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('local', 'away', 'local_goals', 'away_goals', 'date', 'time')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('type', 'minute', 'player', 'second_player')

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        local = game.local
        away = game.away
        self.fields['player'].queryset = Player.objects.filter(Q(team=local) | Q(team=away))
        self.fields['second_player'].queryset = Player.objects.filter(Q(team=local) | Q(team=away))

    def save(self, *args, **kwargs):
        event = super().save(commit=False)
        event.game = self.game
        event = super().save(*args, **kwargs)
        return event