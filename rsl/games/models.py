from django.db import models
from players.models import Player

class Game(models.Model):
    local = models.ForeignKey('tournament.Team', related_name='local_games', on_delete=models.CASCADE)
    away = models.ForeignKey('tournament.Team', related_name='away_games', on_delete=models.CASCADE)
    local_goals = models.SmallIntegerField(default=0)
    away_goals = models.SmallIntegerField(default=0)
    date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return f'{self.local} {self.local_goals} - {self.away_goals} {self.away}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            for player in self.local.players.all():
                player.played += 1
                player.save(update_fields=['played'])

            for player in self.away.players.all():
                player.played += 1
                player.save(update_fields=['played'])

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        for event in Event.objects.filter(game=self):
            event.delete()
        for player in self.local.players.all():
                player.played -= 1
                player.save(update_fields=['played'])

        for player in self.away.players.all():
            player.played -= 1
            player.save(update_fields=['played'])
        super().delete(*args, **kwargs)


class Event(models.Model):
    game = models.ForeignKey('games.Game', related_name='events', on_delete=models.CASCADE)
    minute = models.SmallIntegerField(default=00)
    player = models.ForeignKey('players.Player', related_name='events', on_delete=models.CASCADE)
    second_player = models.ForeignKey(
        'players.Player', related_name='sp_events', on_delete=models.CASCADE, blank=True, null=True
    )

    GOAL = 'GL'
    OWN_GOAL = 'OG'
    PENALTI_GOAL = 'PG'
    CHANGE = 'CG'
    YELLOW_CARD = 'YC'
    RED_CARD = 'RC'
    TYPE = {
        GOAL: 'Gol',
        OWN_GOAL: 'Autogol',
        PENALTI_GOAL: 'Gol de penalti',
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
            case 'PG':
                emote = '⚽️ (P)'
            case 'YC':
                emote = '🟨'
            case 'RC':
                emote = '🟥'
        return f'{emote} {self.player.user.first_name} {self.minute}\''

    def save(self, *args, **kwargs):
        match self.type:
            case 'GL':
                self.player.goals += 1
                if self.second_player:
                    self.second_player.assists += 1
                    self.second_player.save(update_fields=['assists'])
                if self.player.team == self.game.local:
                    self.game.local_goals += 1
                elif self.player.team == self.game.away:
                    self.game.away_goals += 1
            case 'OG':
                if self.player.team == self.game.local:
                    self.game.away_goals += 1
                elif self.player.team == self.game.away:
                    self.game.local_goals += 1
            case 'PG':
                self.player.goals += 1
                if self.player.team == self.game.local:
                    self.game.local_goals += 1
                elif self.player.team == self.game.away:
                    self.game.away_goals += 1
            case 'YC':
                self.player.yellow_cards += 1
            case  'RC':
                self.player.red_cards += 1
        self.player.save(update_fields=['goals', 'yellow_cards', 'red_cards'])
        self.game.save(update_fields=['local_goals', 'away_goals'])
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        match self.type:
            case 'GL':
                self.player.goals -= 1
                if self.second_player:
                    self.second_player.assists -= 1
                    self.second_player.save(update_fields=['assists'])
                if self.player.team == self.game.local:
                    self.game.local_goals -= 1
                elif self.player.team == self.game.away:
                    self.game.away_goals -= 1
            case 'OG':
                if self.player.team == self.game.local:
                    self.game.away_goals -= 1
                elif self.player.team == self.game.away:
                    self.game.local_goals -= 1
            case 'PG':
                self.player.goals -= 1
                if self.player.team == self.game.local:
                    self.game.local_goals -= 1
                elif self.player.team == self.game.away:
                    self.game.away_goals -= 1
            case 'YC':
                self.player.yellow_cards -= 1
            case  'RC':
                self.player.red_cards -= 1
        self.player.save(update_fields=['goals', 'yellow_cards', 'red_cards'])
        self.game.save(update_fields=['local_goals', 'away_goals'])
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['minute']
