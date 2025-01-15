from django.core.management.base import BaseCommand, CommandError

from tournament.models import Clasification


class Command(BaseCommand):
    help = 'Clear all the clasification stats.'

    def handle(self, *args, **options):
        for clasif in Clasification.objects.all():
            clasif.clear_clasification_stats()

            self.stdout.write(
                self.style.SUCCESS('All the teams stats has been cleaned')
            )