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
