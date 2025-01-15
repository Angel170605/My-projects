from django.core.management.base import BaseCommand, CommandError

from players.models import Player


class Command(BaseCommand):
    help = 'Clear all the players stats.'

    def handle(self, *args, **options):
        for player in Player.objects.all():
            player.clear_player_stats()

            self.stdout.write(
                self.style.SUCCESS('All the players stats has been cleaned')
            )