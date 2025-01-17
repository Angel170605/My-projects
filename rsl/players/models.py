from django.conf import settings
from django.db import models

from tournament.models import Team

class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='players', default='players/default.png')
    team = models.ForeignKey('tournament.Team', related_name='players', null=True, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=20, default='🇪🇸')
    number = models.SmallIntegerField(blank=True, default=00)

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
        return f'{self.user.first_name} {self.user.last_name}, #{self.number}'
    
    class Meta:
        ordering = ['team', 'position', 'number']

    def count_goal(self, add: bool, second_player=None):
        if add:
            self.goals += 1
            if second_player:
                second_player.assists += 1
        elif not add:
            self.goals -= 1
            if second_player:
                second_player.assists -= 1

        self.save(update_fields=['goals'])
        if second_player:
            second_player.save(update_fields=['assists'])

    def count_yellow_card(self, add: bool):
        if add:
            self.yellow_cards += 1
        elif not add:
            self.yellow_cards -= 1
        
        self.save(update_fields=['yellow_cards'])

    def count_red_card(self, add: bool):
        if add:
            self.red_cards += 1
        elif not add:
            self.red_cards -= 1
        
        self.save(update_fields=['red_cards'])

    def clear_player_stats(self):
        self.played = 0
        self.goals = 0
        self.assists = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.save()