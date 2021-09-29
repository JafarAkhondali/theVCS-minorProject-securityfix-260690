from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='colorsInImage'),
    path('findColors/', views.findColors, name='findColors'),
]
