from django import forms

from .models import Player

class SignPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('number', 'position')