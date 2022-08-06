from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm

# from django.http.response import HttpResponse

# Create your views here.
"""Rell added logic from tutorial, created a new function call home taking in the request object, returning 
    an HTTP Response Object"""


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User not found")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User or Password not found")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            try:
                user.save()
                login(request, user)
                return redirect('home')
            except:
                messages.error(request, "Could not save user")
        else:
            messages.error(request, "Problem Registering User")

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    # return HttpResponse('Home Page')
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    rooms_count = rooms.count()
    room_messages = Message.objects.all()[:15]

    # the topic__name looks at the topic foreign key object within the
    # room object, and then uses that topic object to query the name

    topics = Topic.objects.all()
    # .order_by('-updated', '-created')
    # This objects method is part of the models object
    # which is a database manager that will return all. notice you can call multiple methods on the same object
    # in the same line
    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count, 'room_messages': room_messages}
    return render(request, 'Base/Home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by('-created')  # This is the most important thing about django query
    # sets. room doesn't even
    # have a message object or attribute, but message has a room object that is of foreign key. Getting all the
    # messages you access the _set of tht foreign key object. Stupid.
    participants = room.participants.all()

    if request.method == 'POST':
        messsage = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('user_room', pk=room.id)

    if request.user.is_authenticated:
        user_messages = request.user.message_set.all().order_by('-created')  # Here's an example of getting all user
    else:
        user_messages = None
    # messages from foreign keys

    context = {'room': room, 'room_messages': messages, 'user_messages': user_messages, 'participants': participants}
    # print(context.get('room').get('name')) """ This line illustrates how to get values from within a dictionary"""
    return render(request, 'Base/Room.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/Delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == "POST":
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'base/Delete.html', context)


"""Adding activity feed"""
