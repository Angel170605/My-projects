from django.db import models
from django.urls import reverse


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    club_code = models.CharField(max_length=3, unique=True, default='UFC')
    shield = models.ImageField(upload_to='shields')

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('tournament:team-info', kwargs={'club_code': self.club_code})


class Match(models.Model):
    local = models.ForeignKey(Team, related_name='local_matches', on_delete=models.CASCADE)
    away = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    local_goals = models.SmallIntegerField(null=True, blank=True)
    away_goals = models.SmallIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.local} {self.local_goals} - {self.away_goals} {self.away}'
