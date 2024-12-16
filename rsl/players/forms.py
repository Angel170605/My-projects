from django import forms

from .models import Player

class SignPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('birthdate', 'country', 'number', 'position', 'photo')
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

class EditPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('birthdate', 'country', 'number', 'position', 'photo')
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }