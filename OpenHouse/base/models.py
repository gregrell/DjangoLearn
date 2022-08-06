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
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)  # Any time the save method is called, this will auto populate
    created = models.DateTimeField(auto_now_add=True)  # The difference between auto_now and auto_add_now is that

    # auto_now will take a timestampe every time, and auto_now_add will only do a timestamp when the instance is
    # created ie. only the creation timestamp

    class Meta:
        # Meta classes are used to add additional parameters to a django class. They have predefined attribute values
        ordering = ['-updated', '-created']
        # db_table = 'some other table name other than the model name'
        # app_label = 'my app name, to override the app name'
        # base_manager_name = 'something' is the name to use for the base manager attribute ie. object.get_all()
        # now becomes something.get_all()
        # get_latest_by = 'some field' will specify how to get the latest by the object.latest() and earliest()
        # methods

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Cascade means if the foreign key is deleted, this
    # entry will also be deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]  # Return only the first 50 characters
