from django.shortcuts import render, redirect

from .models import Room, Topic
from .forms import RoomForm

# from django.http.response import HttpResponse

# Create your views here.
"""Rell added logic from tutorial, created a new function call home taking in the request object, returning 
    an HTTP Response Object"""


def home(request):
    # return HttpResponse('Home Page')
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)

    # the topic__name looks at the topic foreign key object within the
    # room object, and then uses that topic object to query the name

    topics = Topic.objects.all()
    # .order_by('-updated', '-created')
    # This objects method is part of the models object
    # which is a database manager that will return all. notice you can call multiple methods on the same object
    # in the same line
    context = {'rooms': rooms, 'topics':topics}
    return render(request, 'Base/Home.html', context)


def room(request, pk):
    room = None
    room = Room.objects.get(id=pk)
    context = {'room': room}
    # print(context.get('room').get('name')) """ This line illustrates how to get values from within a dictionary"""
    return render(request, 'Base/Room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)  # ALWAYS POPULATE YOUR form object with the post data

        if form.is_valid():
            form.save()

            return redirect('home')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()

        return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method=="POST":
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request,'base/Delete.html', context)


