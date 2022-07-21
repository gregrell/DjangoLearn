from django.shortcuts import render

# from django.http.response import HttpResponse

# Create your views here.
"""Rell added logic from tutorial, created a new function call home taking in the request object, returning 
    an HTTP Response Object"""


def home(request):
    # return HttpResponse('Home Page')
    return render(request, 'Home.html')


def room(request):
    return render(request, 'Room.html')
