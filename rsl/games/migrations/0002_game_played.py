# Generated by Django 5.1.3 on 2024-12-01 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='played',
            field=models.BooleanField(default=False),
        ),
    ]
