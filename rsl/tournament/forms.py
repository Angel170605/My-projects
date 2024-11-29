from django import forms

from .models import Team
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

class PlayerStatsForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('goals', 'assists', 'yellow_cards', 'red_cards')