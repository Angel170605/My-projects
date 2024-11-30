from django import forms

from .models import Team, Match, Event
from players.models import Player


class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            'name',
            'club_code',
            'shield',
        )


class EditTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            'name',
            'club_code',
            'shield',
        )

class SignPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('number', 'position')

class AddMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('local', 'away', 'local_goals', 'away_goals', 'date',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('type', 'minute', 'player', 'second_player',)
