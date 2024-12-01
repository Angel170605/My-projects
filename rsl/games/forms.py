from django import forms

from .models import Game, Event

class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('local', 'away', 'local_goals', 'away_goals', 'date',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class EditGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('local', 'away', 'local_goals', 'away_goals', 'date',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('type', 'minute', 'player', 'second_player',)

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('type', 'minute', 'player', 'second_player',)