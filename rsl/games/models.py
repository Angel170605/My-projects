from django.db import models
from players.models import Player

class Game(models.Model):
    local = models.ForeignKey('tournament.Team', related_name='local_games', on_delete=models.CASCADE)
    away = models.ForeignKey('tournament.Team', related_name='away_games', on_delete=models.CASCADE)
    local_goals = models.SmallIntegerField(default=0)
    away_goals = models.SmallIntegerField(default=0)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    is_league_game = models.BooleanField(default=False)
    TO_PLAY = 'T'
    IN_GAME = 'I'
    FINISHED = 'F'
    GAME_STATUS = {
        TO_PLAY: 'Pendiente',
        IN_GAME: 'En juego',
        FINISHED: 'Finalizado'
    }

    status = models.CharField(
        max_length=1,
        choices=GAME_STATUS,
        default=TO_PLAY,
    )

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

            if self.is_league_game:
               self.local.clasification.played += 1
               self.away.clasification.played += 1
               self.local.clasification.save(update_fields=['played'])
               self.away.clasification.save(update_fields=['played'])

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

        if self.is_league_game:
            self.local.clasification.played -= 1
            self.away.clasification.played -= 1
            self.local.clasification.save(update_fields=['played'])
            self.away.clasification.save(update_fields=['played'])
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
        local = self.game.local
        away = self.game.away
        game = self.game
        player = self.player
        second_player = self.second_player

        match self.type:
            case 'GL':
                player.goals += 1
                if second_player:
                    second_player.assists += 1
                    second_player.save(update_fields=['assists'])
                if player.team == local:
                    game.local_goals += 1
                    if game.is_league_game:
                        local.clasification.goals_scored += 1
                        away.clasification.goals_conceded += 1
                elif player.team == away:
                    game.away_goals += 1
                    if game.is_league_game:
                        away.clasification.goals_scored += 1
                        local.clasification.goals_conceded += 1
            case 'OG':
                if player.team == local:
                    game.away_goals += 1
                elif player.team == away:
                    game.local_goals += 1
            case 'PG':
                player.goals += 1
                if player.team == local:
                    game.local_goals += 1
                elif player.team == away:
                    game.away_goals += 1
            case 'YC':
                player.yellow_cards += 1
            case  'RC':
                player.red_cards += 1

        player.save(update_fields=['goals', 'yellow_cards', 'red_cards'])
        game.save(update_fields=['local_goals', 'away_goals'])
        local.clasification.save(update_fields=['goals_scored', 'goals_conceded', 'goals_difference'])
        away.clasification.save(update_fields=['goals_scored','goals_conceded', 'goals_difference'])
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        local = self.game.local
        away = self.game.away
        game = self.game
        player = self.player
        second_player = self.second_player

        match self.type:
            case 'GL':
                player.goals -= 1
                if second_player:
                    second_player.assists -= 1
                    second_player.save(update_fields=['assists'])
                if player.team == local:
                    game.local_goals -= 1
                    if game.is_league_game:
                        local.clasification.goals_scored -= 1
                        away.clasification.goals_conceded -= 1
                elif player.team == away:
                    game.away_goals -= 1
                    if game.is_league_game:
                        away.clasification.goals_scored -= 1
                        local.clasification.goals_conceded -= 1
            case 'OG':
                if player.team == local:
                    game.away_goals -= 1
                    if game.is_league_game:
                       local.clasification.goals_scored -= 1
                       away.clasification.goals_conceded -= 1
                elif player.team == away:
                    game.local_goals -= 1
                    if game.is_league_game:
                        away.clasification.goals_scored -= 1
                        local.clasification.goals_conceded -= 1
            case 'PG':
                player.goals -= 1
                if player.team == local:
                    game.local_goals -= 1
                    if game.is_league_game:
                       local.clasification.goals_scored -= 1
                       away.clasification.goals_conceded -= 1
                elif player.team == away:
                    game.away_goals -= 1
                    if game.is_league_game:
                        away.clasification.goals_scored -= 1
                        local.clasification.goals_conceded -= 1
            case 'YC':
                player.yellow_cards -= 1
            case  'RC':
                player.red_cards -= 1
        player.save(update_fields=['goals', 'yellow_cards', 'red_cards'])
        game.save(update_fields=['local_goals', 'away_goals'])
        local.clasification.save(update_fields=['goals_scored', 'goals_conceded'])
        away.clasification.save(update_fields=['goals_scored', 'goals_conceded'])
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['minute']
