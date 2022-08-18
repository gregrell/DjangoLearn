from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
from . models import Room, Topic, Message, User


admin.site.register(Room)  # This will register the model to be used in the admin page so we can interact with the
# data (from the admin page)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)
