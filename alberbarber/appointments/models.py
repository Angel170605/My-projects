from django.db import models


class Appointment(models.Model):
    date = models.DateTimeField(unique=True)

    def __str__(self):
        return self.date
