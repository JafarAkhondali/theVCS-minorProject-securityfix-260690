from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='homePricePrediction'),
    path('getAddress/', views.getAddress, name='allAddresses'),
    path('getPrice/', views.getPrice, name='getPrice'),
]
