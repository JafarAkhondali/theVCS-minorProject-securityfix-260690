
from django.contrib import admin
from django.urls import path
from django.conf import settings
from olympiansRecognizer import views

urlpatterns = [
    path('', views.home, name='olympiansRecognizer'),
    path('classifyImage/', views.classifyImage, name='classifyImage'),
]
