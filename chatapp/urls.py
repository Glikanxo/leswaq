from django.urls import path
from .views import *


app_name = 'chat'


urlpatterns = [
    path('chat', index, name='index'),
    path('chats/<str:room_name>/', room, name='room'),
]
