from django.db import models


class Game(models.Model):
    local = models.ForeignKey(
        'tournament.Team', related_name='local_games', on_delete=models.CASCADE
    )
    away = models.ForeignKey('tournament.Team', related_name='away_games', on_delete=models.CASCADE)
    local_goals = models.SmallIntegerField(default=0)
    away_goals = models.SmallIntegerField(default=0)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    pointed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return f'{self.local} {self.local_goals} - {self.away_goals} {self.away}'

    def point_game(self):
        local = self.local
        away = self.away
        local_goals = self.local_goals
        away_goals = self.away_goals
        if not self.pointed:
            self.pointed = True
            add = True
        else:
            self.pointed = False
            add = False
        if local_goals > away_goals:
            local.clasification.count_win(add)
            away.clasification.count_lose(add)
        elif local_goals == away_goals:
            local.clasification.count_draw(add)
            away.clasification.count_draw(add)
        elif local_goals < away_goals:
            local.clasification.count_lose(add)
            away.clasification.count_win(add)
        self.save(update_fields=['pointed'])


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

    def count_game_goal(self, add: bool):
        local = self.game.local
        away = self.game.away
        if add:
            oper = 1
        elif not add:
            oper = -1
        if self.player.team == self.game.local:
            local.clasification.goals_scored += oper
            away.clasification.goals_conceded += oper
            self.game.local_goals += oper
        elif self.player.team == self.game.away:
            away.clasification.goals_scored += oper
            local.clasification.goals_conceded += oper
            self.game.away_goals += oper
        local.clasification.save(
            update_fields=['goals_scored', 'goals_conceded', 'goals_difference']
        )
        away.clasification.save(
            update_fields=['goals_scored', 'goals_conceded', 'goals_difference']
        )
        self.game.save(update_fields=['local_goals', 'away_goals'])

    def count_own_goal(self, add: bool):
        local = self.game.local
        away = self.game.away
        if add:
            oper = 1
        elif not add:
            oper = -1
        if self.player.team == self.game.local:
            away.clasification.goals_scored += oper
            local.clasification.goals_conceded += oper
            self.game.away_goals += oper
        elif self.player.team == self.game.away:
            local.clasification.goals_scored += oper
            away.clasification.goals_conceded += oper
            self.game.local_goals += oper
        local.clasification.save(
            update_fields=['goals_scored', 'goals_conceded', 'goals_difference']
        )
        away.clasification.save(
            update_fields=['goals_scored', 'goals_conceded', 'goals_difference']
        )
        self.game.save(update_fields=['local_goals', 'away_goals'])

    def __str__(self) -> str:
        match self.type:
            case 'CG':
                return f"{self.player.user.first_name} ↕️ {self.second_player.user.first_name} {self.minute}'"
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
        return f"{emote} {self.player.user.first_name} {self.minute}'"

    class Meta:
        ordering = ['minute']
