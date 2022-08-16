
from django.urls import path
from . import views  # the . notation here indicates we are importing from the same folder as this file

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>', views.getRoom)

]
