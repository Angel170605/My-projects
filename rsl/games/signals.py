from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Game, Event

@receiver(post_save, sender=Game)
def count_new_match(sender, instance, created, **kwargs):
    local = instance.local
    away = instance.away
    if created:
        local.clasification.played += 1
        away.clasification.played += 1
        local.clasification.save(update_fields=['played'])
        away.clasification.save(update_fields=['played'])

        for player in local.players.all():
            player.played += 1
            player.save(update_fields=['played'])

        for player in away.players.all():
            player.played += 1
            player.save(update_fields=['played'])


@receiver(pre_delete, sender=Game)
def discount_deleted_match(sender, instance, **kwargs):
    local = instance.local
    away = instance.away
    local.clasification.played -= 1
    away.clasification.played -= 1
    local.clasification.save(update_fields=['played'])
    away.clasification.save(update_fields=['played'])

    for player in local.players.all():
            player.played -= 1
            player.save(update_fields=['played'])

    for player in away.players.all():
        player.played -= 1
        player.save(update_fields=['played'])

    if instance.pointed:
         instance.point_match(add=False)


@receiver(post_save, sender=Event)
def aply_event_stats(sender, instance, created, **kwargs):
    player = instance.player
    second_player = instance.second_player
    add = True 

    if created:
        match instance.type:
            case 'GL' | 'PG':
                  instance.count_game_goal(add=add)
                  player.count_goal(add=add, second_player=second_player)
            case 'OG':
                    instance.count_own_goal(add=add)
            case 'YC':
                  player.count_yellow_card(add=add)
            case 'RC':
                  player.count_red_card

@receiver(pre_delete, sender=Event)
def delete_event_stats(sender, instance, **kwargs):
    player = instance.player
    second_player = instance.second_player
    add = False 

    match instance.type:
        case 'GL' | 'PG':
              instance.count_game_goal(add=add)
              player.count_goal(add=add, second_player=second_player)
        case 'OG':
                instance.count_own_goal(add=add)
        case 'YC':
              player.count_yellow_card(add=add)
        case 'RC':
              player.count_red_card