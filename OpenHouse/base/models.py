from django.db import models
from django.contrib.auth.models import User  # Default User model included in Django


# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # On delete of the user, this field is set
    # to null
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)  # the null input arguments allow the database to have a
    # blank value on creation, and on saving. It is set to False by default.
    # participants =
    updated = models.DateTimeField(auto_now=True)  # Any time the save method is called, this will auto populate
    created = models.DateTimeField(auto_now_add=True)  # The difference between auto_now and auto_add_now is that

    # auto_now will take a timestampe every time, and auto_now_add will only do a timestamp when the instance is
    # created ie. only the creation timestamp

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Cascade means if the foreign key is deleted, this
    # entry will also be deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]  # Return only the first 50 characters
