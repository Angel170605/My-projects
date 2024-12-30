# Generated by Django 5.1.3 on 2024-12-30 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0011_game_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('<django.db.models.fields.DateField>, <django.db.models.fields.TimeField>', 'Por jugar'), ('En juego', 'En juego'), ('Finalizado', 'Finalizado')], default='<django.db.models.fields.DateField>, <django.db.models.fields.TimeField>', max_length=150),
        ),
    ]
