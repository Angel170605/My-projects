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

    def get_absolute_url(self):
        return reverse('tournament:team-info', kwargs={'club_code': self.club_code})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Clasification.objects.create(team=self)
    
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
        ordering = ['-points', '-goals_difference', '-team']

    def __str__(self):
        return f'{self.points} {self.played} {self.wins} {self.draws} {self.loses} {self.goals_scored} {self.goals_conceded} {self.goals_difference}'
    
