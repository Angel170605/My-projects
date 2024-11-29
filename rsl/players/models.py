from django.conf import settings
from django.db import models


class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey('tournament.Team', related_name='players', null=True, on_delete=models.CASCADE)
    number = models.SmallIntegerField(blank=True, unique=True, default=00)

    GOALKEEPER = 'GK'
    DEFENDER = 'DF'
    MIDFIELDER = 'MD'
    FORWARD = 'FW'
    ROLE = {
        GOALKEEPER: 'Portero',
        DEFENDER: 'Defensa',
        MIDFIELDER: 'Centrocampista',
        FORWARD: 'Delantero'
    }

    position = models.CharField(
        max_length=2,
        choices=ROLE,
        default=MIDFIELDER,
    )

    played=models.SmallIntegerField(default=0)
    goals=models.SmallIntegerField(default=0)
    assists = models.SmallIntegerField(default=0)
    yellow_cards = models.SmallIntegerField(default=0)
    red_cards = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user}, {self.position}, #{self.number}'