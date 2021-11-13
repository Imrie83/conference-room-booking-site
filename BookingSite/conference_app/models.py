from django.db import models
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=25, unique=True)
    capacity = models.IntegerField()
    # availability = models.BooleanField(null=False, default=True)
    projector = models.BooleanField(null=False, default=False)


    def reserved_today(self):
        today = datetime.now().strftime('%Y-%m-%d')
        reserved_today = self.reservation_set.filter(date=today)
        return reserved_today

    def reservation_list(self):
        today = datetime.now().strftime('%Y-%m-%d')
        reservation_list = self.reservation_set.filter(date__gt=today)
        return reservation_list

    def __str__(self):
        return f'{self.name} / {self.capacity}'

class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)
    comment = models.CharField(max_length=250)

    class Meta:
        unique_together = ('date', 'id')

    def __str__(self):
        return f'{self.room} - {self.date}'

