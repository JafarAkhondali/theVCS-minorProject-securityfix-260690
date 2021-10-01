from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='salaryPredictor'),
    path('getWorkClass', views.getWorkClass, name='getWorkClass'),
    path('getEducation', views.getEducation, name='getEducation'),
    path('getMartialStatus', views.getMartialStatus, name='getMartialStatus'),
    path('getOccupation', views.getOccupation, name='getOccupation'),
    path('getRelationship', views.getRelationship, name='getRelationship'),
    path('getRace', views.getRace, name='getRace'),
    path('getCountry', views.getCountry, name='getCountry'),
    path('predictSalary', views.predict, name='predictSalary'),
]
