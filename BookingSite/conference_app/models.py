from django.db import models


class Room(models.Model):
    name = models.TextField(max_length=25, unique=True)
    capacity = models.IntegerField()
    availability = models.BooleanField(null=False, default=True)
