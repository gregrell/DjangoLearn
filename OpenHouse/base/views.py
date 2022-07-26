from django.shortcuts import render
from .models import Room
from .forms import RoomForm


# from django.http.response import HttpResponse

# Create your views here.
"""Rell added logic from tutorial, created a new function call home taking in the request object, returning 
    an HTTP Response Object"""


def home(request):
    # return HttpResponse('Home Page')
    rooms = Room.objects.all()  # This objects method is part of the models object which is a database manager that
    # will return all
    context = {'rooms': rooms}
    return render(request, 'Base/Home.html', context)


def room(request, pk):
    room = None
    room = Room.objects.get(id=pk)
    context = {'room': room}
    # print(context.get('room').get('name')) """ This line illustrates how to get values from within a dictionary"""
    return render(request, 'Base/Room.html', context)


def createRoom(request):
    form = RoomForm()
    context = {'form': form}
    return render(request, 'base/room_form.html', context)