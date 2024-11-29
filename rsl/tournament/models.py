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
    date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return f'{self.local} {self.local_goals} - {self.away_goals} {self.away}'


class Event(models.Model):
    game = models.ForeignKey(Match, related_name='events', on_delete=models.CASCADE)
    minute = models.SmallIntegerField(default=00)
    player = models.ForeignKey('players.Player', related_name='events', on_delete=models.CASCADE)
    second_player = models.ForeignKey(
        'players.Player', related_name='sp_events', on_delete=models.CASCADE, blank=True
    )

    GOAL = 'GL'
    CHANGE = 'CG'
    YELLOW_CARD = 'YC'
    RED_CARD = 'RC'
    ROLE = {
        GOAL: 'Gol',
        CHANGE: 'Cambio',
        YELLOW_CARD: 'Tarjeta Amarilla',
        RED_CARD: 'Tarjeta Roja',
    }

    type = models.CharField(
        max_length=2,
        choices=ROLE,
        default=GOAL,
    )

    def __str__(self) -> str:
        return f'{self.player} {self.type} {self.minute}'

    class Meta:
        ordering = ['minute']
