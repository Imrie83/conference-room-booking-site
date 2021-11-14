from django.db import models
from datetime import datetime


class Room(models.Model):
    """
    Model stores name, capacity and projector availability
    of a room
    """
    name = models.CharField(max_length=25, unique=True)
    capacity = models.IntegerField()
    projector = models.BooleanField(null=False, default=False)


    def reserved_today(self):
        """
        Based on current date filters object
        reservations equal to the the date

        :return:
        a list of reservations equal to today date
        """
        today = datetime.now().strftime('%Y-%m-%d')
        reserved_today = self.reservation_set.filter(date=today)
        return reserved_today

    def reservation_list(self):
        """
        Takes today date and only leaves reservations
        newer than today

        :return:
        a list of all reservations newer than today
        """
        today = datetime.now().strftime('%Y-%m-%d')
        reservation_list = self.reservation_set.filter(date__gt=today)
        return reservation_list

    def __str__(self):
        return f'{self.name} / {self.capacity}'

class Reservation(models.Model):
    """
    Model stores reservations with date, room id and comments
    """
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)
    comment = models.CharField(max_length=250)

    class Meta:
        unique_together = ('date', 'id')

    def __str__(self):
        return f'{self.room} - {self.date}'

