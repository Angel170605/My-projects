from django import forms

from .models import Game, Event

class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('local', 'away', 'local_goals', 'away_goals', 'date', 'time', 'status', 'is_league_game')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class EditGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('local', 'away', 'local_goals', 'away_goals', 'date', 'time', 'status', 'is_league_game')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('type', 'minute', 'player', 'second_player',)

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('type', 'minute', 'player', 'second_player',)