from django.contrib import admin

# Register your models here.
from . models import Room


admin.site.register(Room)  # This will register the model to be used in the admin page so we can interact with the
# data (from the admin page)

