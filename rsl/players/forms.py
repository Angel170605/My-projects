from django import forms

from .models import Player

class SignPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('birthdate', 'country', 'number', 'position')
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

class EditPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('birthdate', 'country', 'number', 'position', 'played', 'goals', 'assists', 'yellow_cards', 'red_cards')
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }