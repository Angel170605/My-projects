from django.db import models
from django.urls import reverse
from players.models import Player


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
    local_goals = models.SmallIntegerField(default=0)
    away_goals = models.SmallIntegerField(default=0)
    date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return f'{self.local} {self.local_goals} - {self.away_goals} {self.away}'
    
    def save(self, *args, **kwargs):
        for local_player, away_player in zip(Player.objects.filter(team=self.local), Player.objects.filter(team=self.away)):
            local_player.played += 1
            away_player.played += 1
            local_player.save(update_fields=['played'])
            away_player.save(update_fields=['played'])
        super().save(*args, **kwargs)


class Event(models.Model):
    game = models.ForeignKey(Match, related_name='events', on_delete=models.CASCADE)
    minute = models.SmallIntegerField(default=00)
    player = models.ForeignKey('players.Player', related_name='events', on_delete=models.CASCADE)
    second_player = models.ForeignKey(
        'players.Player', related_name='sp_events', on_delete=models.CASCADE, blank=True, null=True
    )

    GOAL = 'GL'
    OWN_GOAL = 'OG'
    CHANGE = 'CG'
    YELLOW_CARD = 'YC'
    RED_CARD = 'RC'
    TYPE = {
        GOAL: 'Gol',
        OWN_GOAL: 'Autogol',
        CHANGE: 'Cambio',
        YELLOW_CARD: 'Tarjeta Amarilla',
        RED_CARD: 'Tarjeta Roja',
    }

    type = models.CharField(
        max_length=2,
        choices=TYPE,
        default=GOAL,
    )

    def __str__(self) -> str:
        match self.type:
            case 'CG':
                return f'{self.player.user.first_name} ↕️ {self.second_player.user.first_name} {self.minute}\''
            case 'GL':
                emote = '⚽️'
            case 'OG':
                emote = '⚽️ (PP)'
            case 'YC':
                emote = '🟨'
            case 'RC':
                emote = '🟥'
        return f'{emote} {self.player.user.first_name} {self.minute}\''
    
    def save(self, *args, **kwargs):
            if self.type == 'GL':
                self.player.goals += 1
                self.second_player.assists += 1
                self.second_player.save(update_fields=['assists'])
                if self.player.team == self.game.local:
                    self.game.local_goals += 1
                elif self.player.team == self.game.away:
                    self.game.away_goals += 1
            if self.type == 'OG':
                if self.player.team == self.game.local:
                    self.game.away_goals += 1
                elif self.player.team == self.game.away:
                    self.game.local_goals += 1
            elif self.type == 'YC':
                self.player.yellow_cards += 1
            elif self.type == 'RC':
                self.player.red_cards += 1
            self.player.save(update_fields=['goals', 'yellow_cards', 'red_cards'])
            self.game.save(update_fields=['local_goals', 'away_goals'])
            super().save(*args, **kwargs)

    class Meta:
        ordering = ['minute']