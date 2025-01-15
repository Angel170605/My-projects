from django.db import models
from django.urls import reverse


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    club_code = models.CharField(max_length=3, unique=True, default='UFC')
    shield = models.ImageField(upload_to='shields', default='shields/default.png')
    info = models.TextField(max_length=1000, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
    
class Clasification(models.Model):
    team = models.OneToOneField('tournament.Team', related_name='clasification', null=True, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    goals_difference = models.IntegerField(default=0)

    class Meta:
        ordering = ['-points', '-played']

    def __str__(self):
        return f'{self.points} {self.played} {self.wins} {self.draws} {self.loses} {self.goals_scored} {self.goals_conceded} {self.goals_difference}'
    
    def count_win(self, add: bool):
        if add:
            self.points += 3
            self.wins += 1
        elif not add:
            self.points -= 3
            self.wins -= 1
        self.save()

    def count_draw(self, add: bool):
        if add:
            self.points += 1
            self.draws += 1
        elif not add:
            self.points -= 1
            self.draws -= 1
        self.save()

    def count_lose(self, add: bool):
        if add:
            self.loses += 1
        elif not add:
            self.loses -= 1
        self.save()

    def clear_clasification_stats(self):
        self.points = 0
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.goals_scored = 0
        self.goals_conceded = 0
        self.goals_difference = 0
        self.save()

