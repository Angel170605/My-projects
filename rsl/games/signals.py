from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Game

@receiver(post_save, sender=Game)
def count_new_match(sender, instance, created, **kwargs):
    if created:
        instance.local.clasification.played += 1
        instance.away.clasification.played += 1
        instance.local.clasification.save(update_fields=['played'])
        instance.away.clasification.save(update_fields=['played'])

@receiver(pre_delete, sender=Game)
def discount_deleted_match(sender, instance, **kwargs):
    instance.local.clasification.played -= 1
    instance.away.clasification.played -= 1
    instance.local.clasification.save(update_fields=['played'])
    instance.away.clasification.save(update_fields=['played'])