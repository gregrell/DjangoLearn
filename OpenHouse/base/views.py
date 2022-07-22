from django.shortcuts import render

# from django.http.response import HttpResponse

# Create your views here.
"""Rell added logic from tutorial, created a new function call home taking in the request object, returning 
    an HTTP Response Object"""

rooms = [
    {'id': 1, 'name': 'Open House Content User 1 - Jamie'},
    {'id': 2, 'name': 'Open House Content User 2 - Vixen'},
    {'id': 3, 'name': 'Open House Content User 3 - Dolly'},

]


def home(request):
    # return HttpResponse('Home Page')
    context = {'rooms': rooms}
    return render(request, 'Base/Home.html', context)


def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    # print(context.get('room').get('name')) """ This line illustrates how to get values from within a dictionary"""
    return render(request, 'Base/Room.html', context)
