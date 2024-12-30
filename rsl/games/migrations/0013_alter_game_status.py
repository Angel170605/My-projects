# Generated by Django 5.1.3 on 2024-12-30 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0012_alter_game_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('Pendiente', 'Por jugar'), ('En juego', 'En juego'), ('Finalizado', 'Finalizado')], default='Pendiente', max_length=25),
        ),
    ]
