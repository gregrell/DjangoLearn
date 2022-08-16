from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

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
            messages.error(request, form.errors)

    context = {'page': page, 'form': form}
    return render(request, 'base/signup.html', context)


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
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q) |
        Q(room__name__icontains=q) |
        Q(user__username__icontains=q) |
        Q(body__icontains=q)
    )

    # the topic__name looks at the topic foreign key object within the
    # room object, and then uses that topic object to query the name

    topics = Topic.objects.all()
    topics_count = topics.count()
    topics = topics[:5]
    # .order_by('-updated', '-created')
    # This objects method is part of the models object
    # which is a database manager that will return all. notice you can call multiple methods on the same object
    # in the same line
    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count, 'room_messages': room_messages, 'topics_count': topics_count}
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
        return redirect('room', pk=room.id)

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
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)  # ALWAYS POPULATE YOUR form object with the post data
        topic, created = Topic.objects.get_or_create(name=request.POST.get('topic'))
        room = Room.objects.create(
            topic = topic,
            host = request.user,
            description = request.POST.get('description'),
            name = request.POST.get('name'),
        )
        return redirect('home')


    context = {'form': form, 'topics': topics}
    return render(request, 'base/create-room.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'room': room}
    return render(request, 'base/create-room.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == "POST":
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'base/delete.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    user_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': user_messages, 'topics': topics}
    return render(request, 'base/User_Profile.html', context)

@login_required(login_url='login')
def updateUser(request,pk):
    user = request.user
    form = UserForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
        else:
            return redirect('home')

    return render(request, 'base/update-user.html', context)

def topics(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

def activities(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)
