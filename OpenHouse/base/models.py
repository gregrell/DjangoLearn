from django.db import models


# Create your models here.
class Room(models.Model):
    # host =
    # topic =
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)  # the null input arguments allow the database to have a
    # blank value on creation, and on saving
    # participants =
    updated = models.DateTimeField(auto_now=True)  # Any time the save method is called, this will auto populate
    created = models.DateTimeField(auto_now_add=True)  # The difference between auto_now and auto_add_now is that

    # auto_now will take a timestampe every time, and auto_now_add will only do a timestamp when the instance is
    # created ie. only the creation timestamp
    def __str__(self):
        return self.name

