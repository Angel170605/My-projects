# Generated by Django 5.1.3 on 2024-11-30 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_alter_player_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='number',
            field=models.SmallIntegerField(blank=True, default=0),
        ),
    ]
