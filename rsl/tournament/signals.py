from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Team, Clasification

@receiver(post_save, sender=Team)
def registrate_team_in_league(sender, instance, created, **kwargs):
    if created:
        Clasification.objects.create(team=instance)
