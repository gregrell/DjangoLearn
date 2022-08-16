"""Created this file to manage url routing within the BASE app itself, and not the OpenHouse Django
    Full project"""


from django.urls import path
from . import views  # the . notation here indicates we are importing from the same folder as this file

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('userProfile/<str:pk>', views.userProfile, name='user-profile'),
    path('updateUser/<str:pk>', views.updateUser, name='update-user'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name="room"),
    path('topics/', views.topics, name="topics"),
    path('activities/', views.activities, name="activities"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message")

]
