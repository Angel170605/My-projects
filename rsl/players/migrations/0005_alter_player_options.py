# Generated by Django 5.1.3 on 2024-11-30 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0004_alter_player_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['position']},
        ),
    ]
