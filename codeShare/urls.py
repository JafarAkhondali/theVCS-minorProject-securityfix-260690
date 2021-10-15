from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='classJoiner'),
    path('saveCode', views.saveCode, name='saveCode'),
    path('getCode', views.getCode, name='getCode'),
]
