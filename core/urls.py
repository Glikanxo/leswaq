from django.contrib import admin
from django.urls import path
from .views import *
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    path('', index, name="index"),
    path('newpost/', newpost, name="new-post"),
    path('notifications/', notifications, name="notifications"),
    path('search/<query>',search, name="search"),
    path('search/',emptysearch, name="emptsearch"),
    path('post/<slug>', post, name='post'),
    path('confirm/<slug>/<pk>', bought_confirm, name='confirm'),
    path('filter/<cat>/<query>/', filtering, name='filter'),
    path('signaler-arnaque', signaler_arnaque, name='signaler-arnaque'),
    path('conditions-generales',conditions, name="conditions"),
    path('politique-confidentialite',politiques, name="politique")
]
