from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=25, unique=True)
    capacity = models.IntegerField()
    availability = models.BooleanField(null=False, default=True)
    projector = models.BooleanField(null=False, default=False)

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

